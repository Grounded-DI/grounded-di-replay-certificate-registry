#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from common import load_json, write_json
from shelter_core import bind_rules


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    result = bind_rules(load_json(args.input))
    write_json(args.output, result)
    print(json.dumps({"stage": "RuleBinder", "status": result["status"], "errors": len(result["errors"])}, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
