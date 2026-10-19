#!/usr/bin/env python3
"""Run the connected ShelterWise stages and write deterministic stage outputs."""

import argparse
import json
from pathlib import Path

from common import load_json, object_sha256, write_json
from shelter_core import allocate, bind_intake, bind_rules, drift_shield, final_chain, ledger_capacity


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output_dir")
    parser.add_argument("--baseline-input", default=None)
    parser.add_argument("--baseline-run", default=None)
    args = parser.parse_args()
    data = load_json(args.input)
    baseline_data = load_json(args.baseline_input or args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    rules = bind_rules(data)
    intake = bind_intake(data, rules)
    ledger = ledger_capacity(data)
    allocation = allocate(data, rules, intake, ledger)
    if args.baseline_run:
        baseline_final = load_json(Path(args.baseline_run) / "final_chain.json")
    else:
        baseline_final = None
    if baseline_final is None:
        baseline_rules = bind_rules(baseline_data)
        baseline_intake = bind_intake(baseline_data, baseline_rules)
        baseline_ledger = ledger_capacity(baseline_data)
        baseline_allocation = allocate(baseline_data, baseline_rules, baseline_intake, baseline_ledger)
        baseline_final = final_chain(baseline_data, baseline_rules, baseline_intake, baseline_ledger, baseline_allocation, {"events": [], "changed_records": [], "changed_outcomes": False})
    drift = drift_shield(data, baseline_data, rules, intake, ledger, allocation, baseline_final)
    final = final_chain(data, rules, intake, ledger, allocation, drift)
    outputs = {
        "rulebinder": rules,
        "intakebinder": intake,
        "capacityledger": ledger,
        "allocationbridge": allocation,
        "driftshield": drift,
        "final_chain": final,
    }
    for name, value in outputs.items():
        write_json(output_dir / f"{name}.json", value)
    summary = {
        "status": "PASS" if final.get("disposition") != "INSUFFICIENT_RECORD" else "INSUFFICIENT_RECORD",
        "disposition": final.get("disposition"),
        "stage_hashes": final.get("stage_hashes"),
        "drift_events": drift.get("events"),
    }
    print(json.dumps(summary, sort_keys=True))
    raise SystemExit(0)


if __name__ == "__main__":
    main()
