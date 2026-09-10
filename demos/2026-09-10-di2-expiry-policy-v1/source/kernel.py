"""Local demo gate v1. No network or application integration."""
import os,re,json
from pathlib import Path
from codec import canonical,sha

BASE_ACTION={'action':'export_report','destination':'approved/report.txt','scope':'demo_directory','state':{'classification':'synthetic','revision':1}}
def integer(x):return type(x) is int and 0<=x<=9007199254740991
def action_valid(x):
    return type(x) is dict and set(x)==set(BASE_ACTION) and all(type(x[k]) is str and x[k] for k in ('action','destination','scope')) and type(x['state']) is dict and set(x['state'])=={'classification','revision'} and type(x['state']['classification']) is str and integer(x['state']['revision'])
def policy_valid(x):
    return type(x) is dict and set(x)==set(BASE_ACTION)|{'version','export_enabled','max_bytes'} and action_valid({k:x[k] for k in BASE_ACTION}) and type(x['version']) is str and bool(x['version']) and type(x['export_enabled']) is bool and integer(x['max_bytes']) and x['max_bytes']>0
def auth_valid(x):
    return type(x) is dict and set(x)==set(BASE_ACTION)|{'policy_sha256','report_sha256','issued_at','expires_at'} and action_valid({k:x[k] for k in BASE_ACTION}) and all(type(x[k]) is str and re.fullmatch('[0-9a-f]{64}',x[k]) for k in ('policy_sha256','report_sha256')) and integer(x['issued_at']) and integer(x['expires_at']) and x['issued_at']<x['expires_at']
def evaluate(report,policy,auth,action,when):
    def deny(reason):return {'decision':'DENY','reason':reason}
    if not policy_valid(policy):return deny('POLICY_INVALID')
    if not auth_valid(auth):return deny('AUTHORIZATION_INVALID')
    if not integer(when):return deny('TIME_INVALID')
    if not action_valid(action):return deny('ACTION_INVALID')
    if sha(canonical(policy))!=auth['policy_sha256']:return deny('POLICY_HASH_MISMATCH')
    if sha(report)!=auth['report_sha256']:return deny('REPORT_HASH_MISMATCH')
    if when<auth['issued_at']:return deny('NOT_YET_VALID')
    if when>=auth['expires_at']:return deny('EXPIRED')
    if any(action[k]!=auth[k] for k in BASE_ACTION):return deny('ACTION_BINDING_MISMATCH')
    if any(action[k]!=policy[k] for k in BASE_ACTION):return deny('POLICY_SCOPE_MISMATCH')
    if canonical(action)!=canonical(BASE_ACTION):return deny('UNSUPPORTED_ACTION')
    if not policy['export_enabled']:return deny('EXPORT_DISABLED')
    if len(report)>policy['max_bytes']:return deny('REPORT_TOO_LARGE')
    return {'decision':'ALLOW','reason':'AUTHORIZED'}

def execute(root,report,policy,auth,action,clock):
    # Freeze supplied records. This does not observe external policy revocation.
    policy,auth,action=json.loads(canonical([policy,auth,action]))
    root=Path(root)
    # Pin the isolated output directory before the final clock sample and gate.
    rootfd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
        os.mkdir('approved',0o700,dir_fd=rootfd)
        dfd=os.open('approved',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=rootfd)
        try:
            when=clock()
            result=evaluate(report,policy,auth,action,when)
            result.update(execution_time=({'invalid_number':repr(when)} if type(when) is float else when),write_open_attempts=0,files={})
            if result['decision']=='DENY':return result
            # Only the allow-listed literal filename is passed to the OS.
            result['write_open_attempts']=1
            fd=os.open('report.txt',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=dfd)
            with os.fdopen(fd,'wb') as out:
                out.write(report);out.flush();os.fsync(out.fileno())
            os.fsync(dfd)
        finally:os.close(dfd)
    finally:os.close(rootfd)
    saved=(root/'approved/report.txt').read_bytes()
    if saved!=report:raise ValueError('EXPORTED_BYTES_MISMATCH')
    result['files']={'approved/report.txt':sha(saved)}
    return result
