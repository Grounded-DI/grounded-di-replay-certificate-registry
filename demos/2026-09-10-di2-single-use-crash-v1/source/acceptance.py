#!/usr/bin/env python3
"""Reverify saved evidence; run new processes/crashes; challenge altered copies."""
import json,shutil,subprocess,sys,tempfile
from pathlib import Path
from codec import canonical,load,save,sha
from reference_check import check,files

def invoke(b):
    p=subprocess.run([sys.executable,'-B',str(b/'verify.py'),str(b)],capture_output=True,text=True,timeout=30)
    return p.returncode,json.loads(p.stdout)
def rehash(snapshot):
    previous='0'*64
    for n,item in enumerate(snapshot['events'],1):
        item['event']['seq']=n;item['event']['previous']=previous
        item['sha256']=sha(canonical(item['event']));previous=item['sha256']
def acceptance(b):
    b=Path(b).resolve();before=files(b)
    code,verified=invoke(b)
    if code:raise ValueError(verified['reason'])
    negatives=[]
    for kind in ('artifact','invented_completion','duplicate_reservation','missing_worker','missing_case','altered_clock'):
        with tempfile.TemporaryDirectory(prefix='di2-history-negative-') as tmp:
            target=Path(tmp)/'bundle';shutil.copytree(b,target)
            if kind=='artifact':
                (target/'evidence/baseline_and_reuse/exports/approved/report-001.txt').write_text('altered synthetic file\n')
            elif kind=='missing_case':shutil.rmtree(target/'evidence/expired')
            else:
                case='crash_after_file' if kind=='invented_completion' else 'twenty_processes' if kind=='missing_worker' else 'baseline_and_reuse'
                path=target/'evidence'/case/'case.json';c=load(path)
                if kind=='invented_completion':
                    e=next(x['event'] for x in c['final_snapshot']['events'] if x['event']['kind']=='UNCERTAIN')
                    e['kind']='COMPLETED';e['to']='COMPLETED';e['detail']={'report_sha256':c['initial_snapshot']['enrollment'][0]['report_sha256']}
                    c['final_snapshot']['states'][e['authorization_id']]='COMPLETED'
                    rehash(c['final_snapshot'])
                elif kind=='duplicate_reservation':
                    e=json.loads(json.dumps(c['final_snapshot']['events'][1]));e['event']['from']='RESERVED'
                    c['final_snapshot']['events'].insert(2,e);rehash(c['final_snapshot'])
                elif kind=='missing_worker':c['workers'].pop()
                else:c['workers'][0]['request']['time']=2000000001000
                save(path,c)
            code,result=invoke(target)
            if code==0:raise ValueError('NEGATIVE_CONTROL_ACCEPTED:'+kind)
            negatives.append({'test':kind,'rejected':True,'exact_reason':result['reason']})
    with tempfile.TemporaryDirectory(prefix='di2-new-schedule-') as tmp:
        out=Path(tmp)/'new-run'
        p=subprocess.run([sys.executable,'-B',str(b/'run_suite.py'),str(out)],capture_output=True,text=True,timeout=45)
        if p.returncode:raise ValueError('NEW_EXPERIMENT_FAILED:'+p.stdout.strip())
        new=json.loads(p.stdout);derived=check(out)
        if len(derived)!=14:raise ValueError('NEW_EXPERIMENT_COVERAGE')
    code,again=invoke(b)
    if code or files(b)!=before:raise ValueError('ORIGINAL_CHANGED_OR_FAILED')
    return {'status':'PASS','saved_history_verification':verified,'negative_controls':negatives,'fresh_experiment':new,'fresh_experiment_reference_check':'PASS','scheduling_byte_identity':'NOT_REQUIRED: a new run may have different process IDs, winner and event order','original_unchanged':True,'original_reverification':'PASS'}
if __name__=='__main__':
    try:print(json.dumps(acceptance(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent),indent=2))
    except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
