import hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[1];bad=[]
for line in (r/"SHA256SUMS.txt").read_text().splitlines():
 d,p=line.split("  ",1);q=r/p
 if not q.exists() or hashlib.sha256(q.read_bytes()).hexdigest()!=d:bad.append(p)
print("OK" if not bad else "FAILED: "+", ".join(bad));raise SystemExit(0 if not bad else 1)
