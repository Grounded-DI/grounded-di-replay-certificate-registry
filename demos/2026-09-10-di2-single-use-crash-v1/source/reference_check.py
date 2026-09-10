"""Reference history checker; imports no gate, worker or suite implementation.
Shared primitives: codec canonical bytes, SHA-256 and strict JSON loader.
"""
from pathlib import Path
from codec import canonical,sha,load
SCENARIOS={'baseline_and_reuse','twenty_processes','two_authorizations','changed_content','changed_destination','expired','changed_policy','missing_store','malformed_schema','corrupted_store','missing_authorization_row','crash_after_reservation','crash_after_file','crash_after_completion'}
FAULTS={'missing_store':'STATE_MISSING','malformed_schema':'OperationalError','corrupted_store':'DatabaseError','missing_authorization_row':'STATE_ENROLLMENT_MISMATCH'}

def need(ok,reason):
    if not ok:raise ValueError(reason)
def files(root):
    out={}
    if Path(root).exists():
        for p in Path(root).rglob('*'):
            need(not p.is_symlink(),'SYMLINK_EVIDENCE')
            if p.is_file():out[p.relative_to(root).as_posix()]=sha(p.read_bytes())
    return out

def binding_reason(q,a):
    if canonical(q['authorization'])!=canonical(a):return 'AUTHORIZATION_BINDING_MISMATCH'
    if sha(q['report'].encode())!=a['report_sha256']:return 'REPORT_HASH_MISMATCH'
    if sha(canonical(q['policy']))!=a['policy_sha256']:return 'POLICY_HASH_MISMATCH'
    if q['policy']!={'version':'single-use-v1','action':'export_report','scope':'demo_directory','export_enabled':True}:return 'POLICY_UNSUPPORTED'
    t=q['time']
    if type(t)!=int or t<a['issued_at'] or t>=a['expires_at']:return 'TIME_INVALID_OR_EXPIRED'
    return None

def history(snap,workers,exports):
    enrolled={a['authorization_id']:a for a in snap['enrollment']}
    need(len(enrolled)==len(snap['enrollment']),'DUPLICATE_ENROLLMENT')
    states={};reserved_by={};prev='0'*64;counts={};byworker={}
    for n,item in enumerate(snap['events'],1):
        e=item['event'];i=e['authorization_id'];kind=e['kind'];worker=e['worker']
        need(set(e)=={'seq','previous','kind','authorization_id','authorization_sha256','from','to','worker','time','detail'},'EVENT_SCHEMA')
        need(e['seq']==n and e['previous']==prev and item['sha256']==sha(canonical(e)),'EVENT_CHAIN')
        need(i in enrolled and e['authorization_sha256']==sha(canonical(enrolled[i])),'ENROLLMENT_BINDING')
        a=enrolled[i];old=states.get(i);need(e['from']==old,'STATE_PREDECESSOR')
        if kind=='ENROLLED':
            need(old is None and e['to']=='UNUSED' and worker=='initializer' and e['time']==a['issued_at'],'BAD_ENROLLMENT_TRANSITION')
        else:
            need(worker in workers,'UNACCOUNTED_EVENT_WORKER')
            q=workers[worker]['request'];need(e['time']==q['time'] and q['authorization']['authorization_id']==i,'REQUEST_EVENT_BINDING')
            reason=binding_reason(q,a);byworker.setdefault(worker,[]).append(e)
            if kind=='RESERVED':
                need(old=='UNUSED' and e['to']=='RESERVED' and reason is None,'INVALID_RESERVATION')
                counts[i]=counts.get(i,0)+1;need(counts[i]==1,'DUPLICATE_CONSUMPTION');reserved_by[i]=worker
            elif kind=='COMPLETED':
                need(old=='RESERVED' and e['to']=='COMPLETED' and worker==reserved_by[i] and reason is None,'INVALID_COMPLETION')
                need(e['detail']=={'report_sha256':a['report_sha256']},'COMPLETION_REPORT_BINDING')
            elif kind=='UNCERTAIN':
                need(old=='RESERVED' and e['to']=='UNCERTAIN' and reason is None,'INVALID_UNCERTAINTY_TRANSITION')
                need(e['detail']=={'reason':'RESERVATION_WITHOUT_COMPLETION','observed_report_sha256':exports.get(a['destination'])},'UNCERTAINTY_OBSERVATION')
            elif kind=='REFUSED':
                need(old in ('UNUSED','RESERVED','COMPLETED','UNCERTAIN') and e['to']==old,'REFUSAL_CHANGED_STATE')
                if reason is None:
                    if old=='UNCERTAIN':reason='UNCERTAIN_NO_RETRY'
                    elif old=='COMPLETED':reason='ALREADY_COMPLETED' if exports.get(a['destination'])==a['report_sha256'] else 'COMPLETED_ARTIFACT_INVALID'
                need(reason is not None and e['detail']=={'reason':reason},'REFUSAL_REASON')
            else:raise ValueError('UNKNOWN_TRANSITION')
        states[i]=e['to'];prev=item['sha256']
    need(states==snap['states'] and set(states)==set(enrolled),'FINAL_STATE_DIVERGENCE')
    return {'states':states,'events':len(snap['events']),'tip':prev,'reservations':sum(counts.values())},byworker

def check_case(path):
    c=load(Path(path)/'case.json');name=c['id'];need(name in SCENARIOS,'UNKNOWN_SCENARIO')
    ws={w['worker']:w for w in c['workers']};need(len(ws)==len(c['workers']),'DUPLICATE_WORKER_ID')
    actual=files(Path(path)/'exports');need(actual==c['exports'],'EXPORT_BYTES_MISMATCH')
    initial,_=history(c['initial_snapshot'],{},{});need(set(initial['states'].values())=={'UNUSED'},'INITIAL_STATE')
    if name in FAULTS:
        need(c['final_snapshot'] is None and c['fault']==name and c['fault_state_hash_before']==c['fault_state_hash_after'],'FAULT_RESET')
        need(not actual and len(ws)==1,'FAULT_EXPORTED')
        w=next(iter(ws.values()));need(w['exit_code']==0 and w['result']=={'worker':w['worker'],'outcome':'REFUSED','reason':FAULTS[name],'write_open_attempts':0},'FAULT_NOT_REFUSED')
        return {'id':name,'status':'PASS','fault_refused':True}
    summary,events=history(c['final_snapshot'],ws,actual)
    need(c['final_snapshot']['enrollment']==c['initial_snapshot']['enrollment'],'ENROLLMENT_CHANGED')
    completed=0;attempts=0
    for namew,w in ws.items():
        ev=events.get(namew,[]);res=w['result']
        if res is None:
            need(w['exit_code']==-9 and name.startswith('crash_') and namew=='crashed','UNACCOUNTED_NO_RESULT');continue
        need(w['exit_code']==0 and res['worker']==namew and ev,'WORKER_RESULT_UNBOUND')
        last=ev[-1]
        if last['kind']=='COMPLETED':expected=('COMPLETED','EXPORTED',1);completed+=1
        elif last['kind']=='UNCERTAIN':expected=('UNCERTAIN','RESERVATION_WITHOUT_COMPLETION',0)
        else:
            need(last['kind']=='REFUSED','INCOMPLETE_WORKER_HISTORY')
            reason=last['detail']['reason'];expected=('ALREADY_COMPLETED' if reason=='ALREADY_COMPLETED' else 'REFUSED',reason,0)
        need((res['outcome'],res['reason'],res['write_open_attempts'])==expected,'WORKER_OUTCOME_DIVERGENCE');attempts+=res['write_open_attempts']
    enrolled=c['final_snapshot']['enrollment']
    allowed={a['destination']:a['report_sha256'] for a in enrolled if c['final_snapshot']['states'][a['authorization_id']]=='COMPLETED'}
    if name=='crash_after_file':allowed={a['destination']:a['report_sha256'] for a in enrolled}
    need(actual==allowed,'UNEXPECTED_EXPORT_SET')
    if name=='twenty_processes':
        need(len(ws)==20 and len({w['pid'] for w in ws.values()})==20 and c['all_workers_ready_before_release'] is True,'CONCURRENCY_PROVENANCE')
        need(completed==1 and attempts==1 and len(actual)==1 and sum(w['result']['outcome']=='ALREADY_COMPLETED' for w in ws.values())==19,'CONCURRENCY_OUTCOMES')
    elif name=='two_authorizations':need(completed==2 and len(actual)==2,'TWO_AUTHORIZATIONS')
    elif name=='baseline_and_reuse':need(completed==1 and attempts==1 and len(ws)==2 and c['same_inode_after_retry'] is True,'BASELINE_REUSE')
    elif name.startswith('crash_'):
        point=name[len('crash_'):];need(c['checkpoint']=={'worker':'crashed','point':point},'CRASH_CHECKPOINT')
        pre=c['snapshot_after_kill'];history(pre,ws,c['exports_after_kill'])
        need(pre['events']==c['final_snapshot']['events'][:len(pre['events'])],'CRASH_HISTORY_PREFIX')
        state='COMPLETED' if point=='after_completion' else 'RESERVED'
        need(set(pre['states'].values())=={state},'CRASH_STATE')
        final='COMPLETED' if point=='after_completion' else 'UNCERTAIN'
        need(set(summary['states'].values())=={final} and actual==c['exports_after_kill'] and c['same_inode_after_recovery'] is True,'RECOVERY_STATE_OR_EFFECT')
        need(len(ws)==3 and attempts==0 and completed==0,'RECOVERY_DUPLICATE_EFFECT')
        need(len(actual)==(0 if point=='after_reservation' else 1),'CRASH_EFFECT_COUNT')
    else:need(not actual and completed==0 and attempts==0 and set(summary['states'].values())=={'UNUSED'},'INVALID_REQUEST_EFFECT')
    return dict(summary,id=name,status='PASS',export_count=len(actual),acknowledged_completions=completed)

def check(root):
    root=Path(root);paths=sorted(root.glob('*/case.json'))
    need({p.parent.name for p in paths}==SCENARIOS,'MISSING_SCENARIO')
    return [check_case(p.parent) for p in paths]
