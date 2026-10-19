#!/usr/bin/env python3
import argparse
import json

from common import load_json, write_json
from shelter_core import allocate, bind_intake, bind_rules, drift_shield, final_chain, ledger_capacity


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("baseline_input")
    parser.add_argument("baseline_final")
    parser.add_argument("output")
    args = parser.parse_args()
    data = load_json(args.input)
    baseline_data = load_json(args.baseline_input)
    baseline_final = load_json(args.baseline_final)
    rules = bind_rules(data)
    intake = bind_intake(data, rules)
    ledger = ledger_capacity(data)
    allocation = allocate(data, rules, intake, ledger)
    result = drift_shield(data, baseline_data, rules, intake, ledger, allocation, baseline_final)
    write_json(args.output, result)
    print(json.dumps({"stage": "DriftShield", "status": result["status"], "events": result["events"]}, sort_keys=True))
    raise SystemExit(0)


if __name__ == "__main__":
    main()
