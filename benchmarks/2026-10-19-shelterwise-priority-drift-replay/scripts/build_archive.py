#!/usr/bin/env python3
"""Build a deterministic ZIP archive of the review package."""

import argparse
import hashlib
import zipfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root")
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    archive = root / "reproducibility_package.zip"
    if archive.exists():
        archive.unlink()
    top = root.name
    excluded = {archive.name, "ARCHIVE_SHA256.txt"}
    files = sorted(path for path in root.rglob("*") if path.is_file() and path.name not in excluded and "__pycache__" not in path.parts and path.suffix != ".pyc")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for path in files:
            relative = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{top}/{relative}")
            info.date_time = (2026, 10, 19, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(info, path.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (root / "ARCHIVE_SHA256.txt").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    print(f"{digest}  {archive.name}")


if __name__ == "__main__":
    main()
