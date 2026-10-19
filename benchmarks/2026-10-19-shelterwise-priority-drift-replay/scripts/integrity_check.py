#!/usr/bin/env python3
"""Verify every file listed in SHA256SUMS.txt."""

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    manifest = root / "SHA256SUMS.txt"
    failures = []
    checked = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        expected, relative = line.split("  ", 1)
        target = root / relative
        if not target.is_file():
            failures.append({"path": relative, "reason": "missing"})
            continue
        observed = sha256(target)
        checked += 1
        if observed != expected:
            failures.append({"path": relative, "reason": "sha256_mismatch", "expected": expected, "observed": observed})
    result = {"status": "PASS" if not failures else "FAIL", "manifest": str(manifest.relative_to(root)), "checked": checked, "failures": failures}
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
