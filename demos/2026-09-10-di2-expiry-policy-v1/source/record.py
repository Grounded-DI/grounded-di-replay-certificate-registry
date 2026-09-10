#!/usr/bin/env python3
"""Generate new evidence into a new directory; never overwrite a release."""
import copy,json,sys,time,tempfile,shutil
from pathlib import Path
from codec import sha,canonical,save
import kernel
from run import run,SOURCES,inventory

def make_case(name,policy,auth,action,when):
    approval={'policy':policy,'authorization':auth,'action':action,'time':auth['issued_at']}
    return copy.deepcopy({'id':name,'approval':approval,'execution':dict(copy.deepcopy(approval),time=when)})
def create_cases(report):
    action=copy.deepcopy(kernel.BASE_ACTION)
    policy=dict(action,version='expiry-policy-v1',export_enabled=True,max_bytes=4096)
    auth=dict(action,policy_sha256=sha(canonical(policy)),report_sha256=sha(report),issued_at=2000000000000,expires_at=2000000001000)
    good=make_case('valid',policy,auth,action,2000000000500)
    cases=[good]
    def case(name):
        c=copy.deepcopy(good);c['id']=name;cases.append(c);return c['execution']
    case('expired')['time']=2000000001001
    case('expiry_boundary')['time']=2000000001000
    case('policy_version_changed')['policy']['version']='expiry-policy-v2'
    case('policy_content_changed_same_version')['policy']['max_bytes']=2048
    for label,key in [('authorization','authorization'),('policy','policy'),('time','time')]:
        del case('missing_'+label)[key]
        case('null_'+label)[key]=None
        case('malformed_'+label)[key]='invalid'
    case('boolean_time')['time']=True
    case('boolean_expiry')['authorization']['expires_at']=True
    case('float_time')['time']=2000000000500.5
    case('reversed_validity')['authorization']['expires_at']=1999999999999
    case('policy_missing_field')['policy'].pop('export_enabled')
    case('policy_extra_field')['policy']['unrecognized']='must reject'
    case('authorization_missing_hash')['authorization'].pop('policy_sha256')
    case('before_issued')['time']=1999999999999
    case('destination_changed')['action']['destination']='changed/report.txt'
    case('valid_again')
    return cases

def real_clock(report,out):
    action=copy.deepcopy(kernel.BASE_ACTION);policy=dict(action,version='expiry-policy-v1',export_enabled=True,max_bytes=4096)
    issued=time.time_ns()//1000000
    auth=dict(action,policy_sha256=sha(canonical(policy)),report_sha256=sha(report),issued_at=issued,expires_at=issued+250)
    approval=kernel.evaluate(report,policy,auth,action,issued)
    start=time.monotonic_ns()
    while time.time_ns()//1000000<auth['expires_at']:
        if time.monotonic_ns()-start>2000000000:raise ValueError('REAL_CLOCK_TIMEOUT')
        time.sleep(0.01)
    waited=time.monotonic_ns()-start
    root=out/'live-clock-sandbox';root.mkdir(mode=0o700)
    result=kernel.execute(root,report,policy,auth,action,lambda:time.time_ns()//1000000)
    if result['decision']!='DENY' or result['reason']!='EXPIRED' or inventory(root):raise ValueError('LIVE_EXPIRY_NOT_REJECTED')
    c=make_case('real_clock_expired',policy,auth,action,result['execution_time'])
    return c,{'clock':'OS wall clock via time.time_ns; Unix milliseconds','wait_clock':'time.monotonic_ns','wait_elapsed_ns':waited,'approval':approval,'execution':result}

def record(out):
    out=Path(out);out.mkdir(mode=0o700,parents=True,exist_ok=False)
    src=Path(__file__).parent
    for n in SOURCES:shutil.copyfile(src/n,out/n)
    report=(src/'report.txt').read_bytes();(out/'report.txt').write_bytes(report)
    # Float is deliberately malformed input; raw JSON input is not canonical identity.
    (out/'cases.json').write_text(json.dumps(create_cases(report),indent=2,sort_keys=True)+'\n')
    real,observed=real_clock(report,out);save(out/'real-clock-case.json',real);save(out/'real-clock-observation.json',observed)
    return run(out,out/'evidence')
if __name__=='__main__':
    try:print(json.dumps({'status':'PASS','sha256':sha(canonical(record(sys.argv[1])))}))
    except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
