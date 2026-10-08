#!/usr/bin/env python3
"""Read-only complete-package verification, including certificate/manifest."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    proc=subprocess.run([sys.executable,'-B',str(ROOT/'source/verify.py')],capture_output=True,text=True)
    if proc.returncode:raise ValueError(proc.stdout)
    result=json.loads(proc.stdout)
    certificate=json.loads((ROOT/'replay-certificate.json').read_text())
    if certificate['disposition']!=result['status'] or certificate['runs']!=result['runs']:
        raise ValueError('CERTIFICATE_RESULT_MISMATCH')
    listed={}
    for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines():
        h,name=line.split(maxsplit=1)
        if name in listed or not (ROOT/name).resolve().is_relative_to(ROOT.resolve()):raise ValueError('BAD_MANIFEST_PATH')
        listed[name]=h
        if digest(ROOT/name)!=h:raise ValueError('MANIFEST_MISMATCH:'+name)
    files={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts}
    if set(listed)!=files:raise ValueError('MANIFEST_COVERAGE')
    expected=files-{'replay-certificate.json'}
    if set(certificate['bound_deliverables'])!=expected:raise ValueError('CERTIFICATE_COVERAGE')
    for name,h in certificate['bound_deliverables'].items():
        if digest(ROOT/name)!=h:raise ValueError('CERTIFICATE_BINDING:'+name)
    return {'status':'PASS','core_verification':'PASS','manifest_entries':len(listed),
        'certificate_bound_deliverables':len(expected),'all_packaged_file_hashes':'PASS',
        'certificate_type':certificate['certificate_type']}

if __name__=='__main__':
    try:print(json.dumps(main(),indent=2))
    except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
