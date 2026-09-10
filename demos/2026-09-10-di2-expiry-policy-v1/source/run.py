#!/usr/bin/env python3
"""Execute recorded input snapshots, using their explicit historical clock values."""
import json,sys,re
from pathlib import Path
from codec import load,save,canonical,sha
import kernel,reference
SOURCES=['codec.py','kernel.py','reference.py','run.py','verify.py','acceptance.py','record.py']
INPUTS=['report.txt','cases.json','real-clock-case.json','real-clock-observation.json']
def inventory(root):
    root=Path(root)
    result={}
    if root.exists():
        for p in root.rglob('*'):
            if p.is_symlink():raise ValueError('SYMLINK_EVIDENCE')
            if p.is_file():result[p.relative_to(root).as_posix()]=sha(p.read_bytes())
    return result

def run(bundle,out):
    bundle=Path(bundle);out=Path(out);out.mkdir(mode=0o700,parents=True,exist_ok=False)
    report=(bundle/'report.txt').read_bytes()
    cases=load(bundle/'cases.json')+[load(bundle/'real-clock-case.json')]
    seen=set();results=[]
    for c in cases:
        name=c['id']
        if not re.fullmatch('[a-z0-9_]+',name) or name in seen:raise ValueError('INVALID_CASE_ID')
        seen.add(name)
        approval=c['approval'];final=c['execution']
        approved=kernel.evaluate(report,approval.get('policy'),approval.get('authorization'),approval.get('action'),approval.get('time'))
        ref_approval=reference.evaluate(report,approval.get('policy'),approval.get('authorization'),approval.get('action'),approval.get('time'))
        if approved!=ref_approval or approved['decision']!='ALLOW':raise ValueError('APPROVAL_FAILED:'+name)
        root=out/'exports'/name;root.mkdir(mode=0o700,parents=True)
        result=kernel.execute(root,report,final.get('policy'),final.get('authorization'),final.get('action'),lambda:final.get('time'))
        ref=reference.evaluate(report,final.get('policy'),final.get('authorization'),final.get('action'),final.get('time'))
        if {'decision':result['decision'],'reason':result['reason']}!=ref:raise ValueError('REFERENCE_DIVERGENCE:'+name)
        if inventory(root)!=result['files']:raise ValueError('FILESYSTEM_DIVERGENCE:'+name)
        results.append({'id':name,'approval':approved,'execution':result,'reference':ref})
    ident={'schema':'DI2-EXPIRY-POLICY-REPLAY-1','canonicalization':'DI2-ASCII-JSON-LF-1',
           'source_hashes':{n:sha((bundle/n).read_bytes()) for n in SOURCES},
           'input_hashes':{n:sha((bundle/n).read_bytes()) for n in INPUTS},'results':results}
    save(out/'results.json',results);save(out/'replay-identity.json',ident)
    (out/'replay-identity.sha256').write_text(sha(canonical(ident))+'\n')
    return ident
if __name__=='__main__':
    try:print(json.dumps({'status':'PASS','sha256':sha(canonical(run(sys.argv[1],sys.argv[2])))}))
    except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
