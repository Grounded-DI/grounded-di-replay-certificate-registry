#!/usr/bin/env python3
import argparse
import json

from common import load_json, write_json
from shelter_core import allocate, bind_intake, bind_rules, ledger_capacity


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    data = load_json(args.input)
    result = allocate(data, bind_rules(data), bind_intake(data, bind_rules(data)), ledger_capacity(data))
    write_json(args.output, result)
    print(json.dumps({"stage": "AllocationBridge", "status": result["status"], "status_counts": result["status_counts"]}, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
