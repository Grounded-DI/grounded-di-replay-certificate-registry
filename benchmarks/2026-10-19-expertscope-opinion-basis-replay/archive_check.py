#!/usr/bin/env python3
import hashlib,sys,tarfile,tempfile
from pathlib import Path
archive=Path(sys.argv[1])
with tarfile.open(archive,"r:gz") as tf:
 members=tf.getmembers()
 if not members or any(Path(m.name).is_absolute() or ".." in Path(m.name).parts for m in members): raise SystemExit("FAIL: invalid archive member")
 with tempfile.TemporaryDirectory() as td:
  tf.extractall(td,filter="data")
  manifests=list(Path(td).rglob("SHA256SUMS.txt"))
  if len(manifests)!=1: raise SystemExit("FAIL: missing or duplicate manifest")
  root=manifests[0].parent
  for line in manifests[0].read_text().splitlines():
   expected,rel=line.split("  ",1); p=root/rel
   if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=expected: raise SystemExit("FAIL: "+rel)
print("PASS: archive opens and embedded manifest verifies")
