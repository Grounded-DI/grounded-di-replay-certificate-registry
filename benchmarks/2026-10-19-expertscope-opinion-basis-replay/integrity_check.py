#!/usr/bin/env python3
import hashlib,sys
from pathlib import Path
root=Path(__file__).resolve().parent
lines=(root/"SHA256SUMS.txt").read_text().splitlines()
errors=[]
for line in lines:
 h,rel=line.split("  ",1); p=root/rel
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=h: errors.append(rel)
print("PASS" if not errors else "FAIL: "+", ".join(errors))
raise SystemExit(bool(errors))
