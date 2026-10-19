#!/usr/bin/env python3
"""Run the four connected synthetic stages in fresh subprocesses."""
import hashlib
import json
import platform
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGES = [
    ("briefwise", "briefwise.py"),
    ("depobot", "depobot.py"),
    ("pidbot", "pidbot.py"),
]


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call(label, script, args, out_dir):
    command = [sys.executable, str(ROOT / script), *[str(value) for value in args]]
    started = utc_now()
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    (out_dir / f"{label}.stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (out_dir / f"{label}.stderr.txt").write_text(completed.stderr, encoding="utf-8")
    return {
        "label": label,
        "command": command,
        "command_display": shlex.join(command),
        "started_utc": started,
        "finished_utc": utc_now(),
        "exit_code": completed.returncode,
        "stdout_file": f"{label}.stdout.txt",
        "stderr_file": f"{label}.stderr.txt",
    }


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: run_chain.py INPUT.json OUTPUT_DIR")
    input_path = Path(sys.argv[1]).resolve()
    out_dir = Path(sys.argv[2]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for label, script in STAGES:
        records.append(call(label, script, [input_path, out_dir / f"{label}.json"], out_dir))
    records.append(call(
        "verdictbridge",
        "verdictbridge.py",
        [input_path, out_dir / "briefwise.json", out_dir / "depobot.json", out_dir / "pidbot.json", out_dir / "final_chain.json"],
        out_dir,
    ))
    final_path = out_dir / "final_chain.json"
    if final_path.exists():
        final = json.loads(final_path.read_text(encoding="utf-8"))
        final_hash = final["final_chain_sha256"]
        disposition = final["disposition"]
    else:
        final_hash = None
        disposition = "EXECUTION_ERROR"
    stage_hashes = {}
    for label, _ in STAGES:
        output = out_dir / f"{label}.json"
        if output.exists():
            stage_hashes[label] = json.loads(output.read_text(encoding="utf-8")).get("canonical_record_sha256")
    execution = {
        "schema": "integrated-chain-execution-v2",
        "input": str(input_path),
        "input_sha256": sha256_file(input_path),
        "python": sys.version,
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "package_root": str(ROOT),
        "stage_execution_count": len(records),
        "stage_runs": records,
        "stage_hashes": stage_hashes,
        "final_chain_sha256": final_hash,
        "disposition": disposition,
        "all_exit_codes_zero": all(item["exit_code"] == 0 for item in records),
    }
    (out_dir / "execution.json").write_text(json.dumps(execution, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    summary = {
        "run": "PASS" if execution["all_exit_codes_zero"] and final_hash else "FAIL",
        "final_chain_sha256": final_hash,
        "disposition": disposition,
        "stage_execution_count": len(records),
    }
    print(json.dumps(summary, sort_keys=True, indent=2))
    raise SystemExit(0 if summary["run"] == "PASS" else 1)


if __name__ == "__main__":
    main()
