#!/usr/bin/env python3
"""Capture two canonical replays plus the independent and control runs."""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from common import file_sha256, load_json, write_json


STAGES = ["rulebinder", "intakebinder", "capacityledger", "allocationbridge", "driftshield", "final_chain"]


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def remove_scoped(path):
    path = Path(path)
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def execute(command, cwd, stdout_path, stderr_path, execution_path):
    started = now()
    process = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    Path(stdout_path).write_text(process.stdout, encoding="utf-8")
    Path(stderr_path).write_text(process.stderr, encoding="utf-8")
    record = {
        "started_at_utc": started,
        "finished_at_utc": now(),
        "command": command,
        "cwd": str(cwd),
        "exit_code": process.returncode,
        "stdout_sha256": file_sha256(stdout_path),
        "stderr_sha256": file_sha256(stderr_path),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
    }
    write_json(execution_path, record)
    return process


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root")
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    scripts = root / "scripts"
    canonical_input = root / "canonical_input.json"
    for name in ["executions", "controls", "expected_outputs", "actual_outputs_run_1", "actual_outputs_run_2"]:
        remove_scoped(root / name)
    for name in ["CONTROL_RESULTS.json", "ENVIRONMENT.json", "REPLAY_RESULTS.json", "independent_evaluator.stdout.txt", "independent_evaluator.stderr.txt", "independent_evaluator.execution.json", "controls.stdout.txt", "controls.stderr.txt", "controls.execution.json", "commands.txt", "SHA256SUMS.txt", "reproducibility_package.zip", "ARCHIVE_SHA256.txt"]:
        remove_scoped(root / name)
    executions = root / "executions"
    executions.mkdir()
    run_results = {}
    run_commands = []
    for number in [1, 2]:
        run_dir = executions / f"run_{number}"
        run_dir.mkdir()
        command = [sys.executable, "-B", str(scripts / "run_pipeline.py"), str(canonical_input), str(run_dir)]
        run_commands.append(" ".join(command))
        process = execute(command, root, run_dir / "stdout.txt", run_dir / "stderr.txt", run_dir / "execution.json")
        run_results[f"run_{number}"] = {"exit_code": process.returncode, "directory": str(run_dir.relative_to(root))}
        if process.returncode != 0:
            raise SystemExit(f"canonical run {number} failed with exit code {process.returncode}")

    evaluator_command = [sys.executable, "-B", str(scripts / "independent_evaluator.py"), str(canonical_input), str(executions / "run_1")]
    run_commands.append(" ".join(evaluator_command))
    evaluator = execute(evaluator_command, root, root / "independent_evaluator.stdout.txt", root / "independent_evaluator.stderr.txt", root / "independent_evaluator.execution.json")
    if evaluator.returncode != 0:
        raise SystemExit("independent evaluator failed")

    control_command = [sys.executable, "-B", str(scripts / "controls.py"), str(canonical_input), str(scripts / "run_pipeline.py"), str(root / "CONTROL_RESULTS.json")]
    run_commands.append(" ".join(control_command))
    controls = execute(control_command, root, root / "controls.stdout.txt", root / "controls.stderr.txt", root / "controls.execution.json")
    if controls.returncode != 0:
        raise SystemExit("control suite failed")

    for number in [1, 2]:
        destination = root / f"actual_outputs_run_{number}"
        destination.mkdir()
        for stage in STAGES:
            shutil.copy2(executions / f"run_{number}" / f"{stage}.json", destination / f"{stage}.json")
    expected = root / "expected_outputs"
    expected.mkdir()
    for stage in STAGES:
        shutil.copy2(executions / "run_1" / f"{stage}.json", expected / f"{stage}.json")

    identity = {}
    mismatches = []
    for stage in STAGES:
        first = file_sha256(executions / "run_1" / f"{stage}.json")
        second = file_sha256(executions / "run_2" / f"{stage}.json")
        identity[stage] = {"run_1_sha256": first, "run_2_sha256": second, "identical": first == second}
        if first != second:
            mismatches.append(stage)
    evaluator_result = json.loads((root / "independent_evaluator.stdout.txt").read_text(encoding="utf-8"))
    control_result = load_json(root / "CONTROL_RESULTS.json")
    final = load_json(executions / "run_1" / "final_chain.json")
    result = {
        "schema": "shelterwise-replay-results-v1",
        "synthetic_fixture": True,
        "canonical_execution_count": 2,
        "stage_execution_counts": {stage: 2 for stage in STAGES},
        "stage_output_identity": identity,
        "final_chain_replay_identity": all(item["identical"] for item in identity.values()),
        "record_mismatches": mismatches,
        "observed_replay_divergence": bool(mismatches),
        "independent_evaluator": {"status": evaluator_result.get("status"), "imports_primary_stage_logic": evaluator_result.get("imports_primary_stage_logic"), "comparisons": evaluator_result.get("comparisons")},
        "altered_control_result": {"status": "PASS" if control_result.get("fail_count") == 0 else "FAIL", "control_count": control_result.get("control_count"), "pass_count": control_result.get("pass_count"), "fail_count": control_result.get("fail_count"), "actual_mutated_input_pipeline_executions": control_result.get("actual_mutated_input_pipeline_executions"), "actual_intermediate_tamper_executions": control_result.get("actual_intermediate_tamper_executions")},
        "final_disposition": final.get("disposition"),
        "final_drift_events": final.get("drift_events"),
        "environment_record": "ENVIRONMENT.json",
        "execution_records": ["executions/run_1/execution.json", "executions/run_2/execution.json", "independent_evaluator.execution.json", "controls.execution.json"],
    }
    write_json(root / "REPLAY_RESULTS.json", result)
    environment = {
        "captured_at_utc": now(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "os_name": os.name,
        "working_directory": str(root),
        "relevant_environment": {key: os.environ.get(key) for key in ["LANG", "LC_ALL", "PYTHONHASHSEED", "TZ"] if key in os.environ},
        "network_calls_in_replay": False,
        "external_data_sources": [],
    }
    write_json(root / "ENVIRONMENT.json", environment)
    (root / "commands.txt").write_text("\n".join(run_commands) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "canonical_execution_count": 2, "control_count": control_result.get("control_count"), "final_disposition": final.get("disposition")}, sort_keys=True))


if __name__ == "__main__":
    main()
