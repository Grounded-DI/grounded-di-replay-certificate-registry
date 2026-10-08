#!/usr/bin/env python3
"""Future reviewer: hash and direct-byte checks only, not substantive verification."""
import hashlib,json,sys
from pathlib import Path
expected=json.loads((Path(__file__).parent/'expected-hashes.json').read_text())['canonical_artifacts']
root=Path(sys.argv[1]); result={}; ok=True
for name,h in expected.items():
 data=[(root/r/name).read_bytes() for r in ('Run-A','Run-B','Run-C')]
 hashes=[hashlib.sha256(d).hexdigest() for d in data]
 row={'sha256':hashes,'expected_match':all(x==h for x in hashes),'direct_bytes_equal':data[0]==data[1]==data[2]}
 result[name]=row;ok=ok and row['expected_match'] and row['direct_bytes_equal']
print(json.dumps({'status':'PASS' if ok else 'FAIL','artifacts':result},indent=2))
sys.exit(0 if ok else 1)
