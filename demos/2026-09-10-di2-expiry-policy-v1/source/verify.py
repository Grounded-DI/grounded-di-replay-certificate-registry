#!/usr/bin/env python3
"""Read-only bundle verification plus fresh isolated execution; no model calls."""
import json,sys,tempfile,subprocess
from pathlib import Path
from codec import load,sha,canonical
from run import inventory

def verify(b):
    b=Path(b).resolve()
    with tempfile.TemporaryDirectory(prefix='di2-expiry-replay-') as tmp:
        out=Path(tmp)/'fresh'
        p=subprocess.run([sys.executable,'-B',str(b/'run.py'),str(b),str(out)],capture_output=True,text=True)
        if p.returncode:raise ValueError('FRESH_RUN_FAILED:'+p.stdout.strip())
        generated=(out/'replay-identity.json').read_bytes();stored=(b/'evidence/replay-identity.json').read_bytes()
        if generated!=stored:raise ValueError('REPLAY_IDENTITY_MISMATCH')
        h=sha(generated)
        if (b/'evidence/replay-identity.sha256').read_text()!=h+'\n':raise ValueError('REPLAY_HASH_MISMATCH')
        if (out/'results.json').read_bytes()!=(b/'evidence/results.json').read_bytes():raise ValueError('SAVED_RESULTS_MISMATCH')
        if inventory(out/'exports')!=inventory(b/'evidence/exports'):raise ValueError('SAVED_EXPORT_MISMATCH')
        real=load(b/'real-clock-observation.json');c=load(b/'real-clock-case.json')
        historical=next(x for x in load(out/'results.json') if x['id']==c['id'])
        if real['execution']!=historical['execution'] or real['approval']!=historical['approval']:raise ValueError('REAL_CLOCK_RECORD_MISMATCH')
        if real['execution']['decision']!='DENY' or real['execution']['reason']!='EXPIRED' or not 0<=real['wait_elapsed_ns']<=3000000000:raise ValueError('REAL_CLOCK_CHECK_FAILED')
        return {'status':'PASS','replay_sha256':h,'canonical_bytes_identical':True,'fresh_process_execution':True,'reference_comparison':'PASS','saved_exports':'PASS','real_clock_historical_replay':'PASS','case_count':len(load(out/'results.json'))}
if __name__=='__main__':
    try:print(json.dumps(verify(sys.argv[1] if len(sys.argv)>1 else Path(__file__).parent),indent=2))
    except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
