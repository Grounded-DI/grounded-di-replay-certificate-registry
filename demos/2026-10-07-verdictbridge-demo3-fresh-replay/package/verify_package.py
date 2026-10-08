#!/usr/bin/env python3
"""Read-only hash/binding verification. Does not execute benchmark code."""
import hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 files={p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()}
 assert not any(p.is_symlink() for p in R.rglob('*')), 'SYMLINK'
 manifest={}
 for line in (R/'SHA256SUMS.txt').read_text().splitlines():
  h,n=line.split('  ',1)
  assert n not in manifest and (R/n).resolve().is_relative_to(R), 'BAD_MANIFEST_PATH'
  assert digest(R/n)==h, 'HASH_MISMATCH:'+n
  manifest[n]=h
 assert set(manifest)==files-{'SHA256SUMS.txt'}, 'MANIFEST_COVERAGE'
 cert=json.loads((R/'replay-certificate.json').read_text())
 assert set(cert['bound_deliverables'])==files-{'SHA256SUMS.txt','replay-certificate.json'}, 'CERTIFICATE_COVERAGE'
 for n,h in cert['bound_deliverables'].items():assert digest(R/n)==h,'BINDING_MISMATCH:'+n
 expected=json.loads((R/'pinned/expected-hashes.json').read_text())
 assert digest(R/'pinned/VerdictBridge_Demo3_Public_v1.zip')==expected['complete_zip_sha256'],'PINNED_ARCHIVE_MISMATCH'
 for n,h in expected['canonical_artifacts'].items():
  paths=[R/'replay'/r/n for r in ['Run-A','Run-B','Run-C']]+[R/'pinned/VerdictBridge_Demo3_Public_v1'/r/n for r in ['Run-A','Run-B','Run-C']]
  assert all(digest(p)==h and p.read_bytes()==paths[0].read_bytes() for p in paths),'CANONICAL_MISMATCH:'+n
 assert cert['disposition']=='PASS'
 return {'status':'PASS','scope':'Integrity/bindings and direct canonical bytes; no semantic execution','manifest_entries':len(manifest),'certificate_bindings':len(cert['bound_deliverables'])}
if __name__=='__main__':
 try:print(json.dumps(main(),indent=2))
 except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
