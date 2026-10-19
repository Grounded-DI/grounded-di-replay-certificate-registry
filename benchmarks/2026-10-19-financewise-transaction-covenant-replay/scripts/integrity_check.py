#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default=None)
    a = p.parse_args()
    root = Path(a.root).resolve() if a.root else Path(__file__).resolve().parent.parent
    manifest = root / "SHA256SUMS.txt"
    failures = []
    checked = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split("  ", 1)
        path = root / rel
        if not path.exists():
            failures.append({"path": rel, "error": "missing"})
            continue
        checked += 1
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            failures.append({"path": rel, "expected": expected, "actual": actual})
    result = {"status": "PASS" if not failures else "FAIL", "manifest": str(manifest), "checked": checked, "failures": failures}
    print(result)
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
