#!/usr/bin/env python3
"""Create the package SHA-256 manifest without self-reference."""

import argparse
import hashlib
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root")
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    excluded = {"SHA256SUMS.txt", "reproducibility_package.zip", "ARCHIVE_SHA256.txt"}
    files = sorted(path for path in root.rglob("*") if path.is_file() and path.name not in excluded and "__pycache__" not in path.parts and path.suffix != ".pyc")
    lines = []
    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
    (root / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifest_entries={len(lines)}")


if __name__ == "__main__":
    main()
