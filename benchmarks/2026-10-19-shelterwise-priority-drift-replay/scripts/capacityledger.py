#!/usr/bin/env python3
import argparse
import json

from common import load_json, write_json
from shelter_core import ledger_capacity


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    result = ledger_capacity(load_json(args.input))
    write_json(args.output, result)
    print(json.dumps({"stage": "CapacityLedger", "status": result["status"], "errors": len(result["errors"]), "duplicate_reservations": len(result["duplicate_reservations"])}, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
