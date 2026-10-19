#!/usr/bin/env python3
import json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAGES = [("briefwise", "briefwise.py"), ("depobot", "depobot.py"), ("pidbot", "pidbot.py")]

def call(label, script, args, out_dir):
    command = [sys.executable, str(ROOT / script), *[str(x) for x in args]]
    started = datetime.now(timezone.utc).isoformat()
    p = subprocess.run(command, capture_output=True, text=True)
    (out_dir / f"{label}.stdout.txt").write_text(p.stdout, encoding="utf-8")
    (out_dir / f"{label}.stderr.txt").write_text(p.stderr, encoding="utf-8")
    return {"label": label, "command": " ".join(command), "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(), "exit_code": p.returncode}

def main():
    input_path, out_dir = Path(sys.argv[1]), Path(sys.argv[2]); out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for label, script in STAGES:
        records.append(call(label, script, [input_path, out_dir / f"{label}.json"], out_dir))
    records.append(call("verdictbridge", "verdictbridge.py", [input_path, out_dir / "briefwise.json", out_dir / "depobot.json", out_dir / "pidbot.json", out_dir / "final_chain.json"], out_dir))
    final = json.loads((out_dir / "final_chain.json").read_text())
    execution = {"schema": "integrated-chain-execution-v1", "input": str(input_path), "python": sys.version.split()[0], "platform": sys.platform, "stage_runs": records, "stage_hashes": {k: json.loads((out_dir / f"{k}.json").read_text())["canonical_record_sha256"] for k in ("briefwise", "depobot", "pidbot")}, "final_chain_sha256": final["final_chain_sha256"]}
    (out_dir / "execution.json").write_text(json.dumps(execution, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run": "PASS" if all(x["exit_code"] == 0 for x in records) else "FAIL", "final_chain_sha256": final["final_chain_sha256"], "disposition": final["disposition"]}, sort_keys=True, indent=2))
    raise SystemExit(0 if all(x["exit_code"] == 0 for x in records) else 1)

if __name__ == "__main__": main()
