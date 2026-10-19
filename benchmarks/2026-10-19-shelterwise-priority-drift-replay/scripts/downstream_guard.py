#!/usr/bin/env python3
"""Reject a downstream allocation record whose bound stage hash changed."""

import argparse
import json
import sys

from common import load_json, object_sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("allocation")
    parser.add_argument("final_chain")
    args = parser.parse_args()
    allocation = load_json(args.allocation)
    final = load_json(args.final_chain)
    observed = object_sha256(allocation)
    expected = final.get("stage_hashes", {}).get("allocationbridge")
    result = {"status": "PASS" if observed == expected else "REJECTED", "observed_hash": observed, "expected_hash": expected}
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if observed == expected else 1)


if __name__ == "__main__":
    main()
