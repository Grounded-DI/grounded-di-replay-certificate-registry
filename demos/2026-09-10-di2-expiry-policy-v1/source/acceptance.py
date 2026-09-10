#!/usr/bin/env python3
"""Fresh replay, explicit expected cases, altered-copy controls, live-clock check."""
import copy,json,shutil,subprocess,sys,tempfile
from pathlib import Path
from codec import canonical,load,sha,save
import kernel,reference
from run import inventory
from record import real_clock

EXPECTED={'valid':'AUTHORIZED','expired':'EXPIRED','expiry_boundary':'EXPIRED','policy_version_changed':'POLICY_HASH_MISMATCH','policy_content_changed_same_version':'POLICY_HASH_MISMATCH','boolean_time':'TIME_INVALID','boolean_expiry':'AUTHORIZATION_INVALID','float_time':'TIME_INVALID','reversed_validity':'AUTHORIZATION_INVALID','policy_missing_field':'POLICY_INVALID','policy_extra_field':'POLICY_INVALID','authorization_missing_hash':'AUTHORIZATION_INVALID','before_issued':'NOT_YET_VALID','destination_changed':'ACTION_BINDING_MISMATCH','valid_again':'AUTHORIZED','real_clock_expired':'EXPIRED'}
for name,reason in [('authorization','AUTHORIZATION_INVALID'),('policy','POLICY_INVALID'),('time','TIME_INVALID')]:
    for prefix in ('missing','null','malformed'):EXPECTED[prefix+'_'+name]=reason

def invoke(b):
    p=subprocess.run([sys.executable,'-B',str(b/'verify.py'),str(b)],capture_output=True,text=True)
    return p.returncode,json.loads(p.stdout)

def acceptance(b):
    b=Path(b).resolve();before=inventory(b)
    c,verified=invoke(b)
    if c:raise ValueError(verified)
    results=load(b/'evidence/results.json')
    if {r['id'] for r in results}!=set(EXPECTED):raise ValueError('CASE_COVERAGE_MISMATCH')
    for r in results:
        x=r['execution'];wanted=EXPECTED[r['id']]
        if x['reason']!=wanted or x['decision']!=('ALLOW' if wanted=='AUTHORIZED' else 'DENY'):raise ValueError('UNEXPECTED_DECISION:'+r['id'])
        if x['write_open_attempts']!=(1 if wanted=='AUTHORIZED' else 0):raise ValueError('UNEXPECTED_WRITE:'+r['id'])
    report=(b/'report.txt').read_bytes();good=load(b/'cases.json')[0]['execution']
    # Agreement across every integer immediately around both boundaries.
    boundary=0
    for t in list(range(1999999999998,2000000000003))+list(range(2000000000998,2000000001003)):
        k=kernel.evaluate(report,good['policy'],good['authorization'],good['action'],t)
        r=reference.evaluate(report,good['policy'],good['authorization'],good['action'],t)
        reason='NOT_YET_VALID' if t<2000000000000 else 'EXPIRED' if t>=2000000001000 else 'AUTHORIZED'
        if k!=r or k['reason']!=reason:raise ValueError('BOUNDARY_CHECK_FAILED')
        boundary+=1
    negatives=[]
    for kind in ('report','expiry_evidence','same_version_policy','saved_export','saved_decision','source_binding'):
        with tempfile.TemporaryDirectory(prefix='di2-altered-copy-') as tmp:
            target=Path(tmp)/'bundle';shutil.copytree(b,target)
            if kind=='report':(target/'report.txt').write_bytes(report+b'ALTERED\n')
            elif kind in ('expiry_evidence','same_version_policy'):
                cases=load(target/'cases.json')
                if kind=='expiry_evidence':cases[0]['execution']['time']=2000000001000
                else:cases[0]['execution']['policy']['max_bytes']=2048
                (target/'cases.json').write_text(json.dumps(cases))
            elif kind=='saved_export':(target/'evidence/exports/valid/approved/report.txt').unlink()
            elif kind=='saved_decision':
                rs=load(target/'evidence/results.json');rs[1]['execution']['decision']='ALLOW';save(target/'evidence/results.json',rs)
            else:
                with (target/'kernel.py').open('a') as f:f.write('\n# altered source\n')
            code,r=invoke(target)
            if code==0:raise ValueError('TAMPER_NOT_REJECTED:'+kind)
            negatives.append({'test':kind,'rejected':True,'reason':r['reason']})
    # Rerun a live expiry separately; its times are not compared with historical times.
    with tempfile.TemporaryDirectory(prefix='di2-live-expiry-') as tmp:
        live,obs=real_clock(report,Path(tmp))
    c,reverified=invoke(b)
    if c or inventory(b)!=before:raise ValueError('ORIGINAL_CHANGED_OR_FAILED')
    return {'status':'PASS','verification':verified,'expected_case_checks':len(EXPECTED),'extra_boundary_checks':boundary,'negative_controls':negatives,'new_real_clock_test':obs,'original_unchanged':True,'original_reverification':'PASS'}
if __name__=='__main__':
    try:print(json.dumps(acceptance(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent),indent=2))
    except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
