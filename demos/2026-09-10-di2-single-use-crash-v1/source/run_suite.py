#!/usr/bin/env python3
"""Fresh multiprocess and SIGKILL tests, always in isolated temporary stores."""
import copy,json,os,shutil,signal,sqlite3,subprocess,sys,tempfile,time
from pathlib import Path
from codec import load,save,sha,canonical
from gate import init_store,snapshot
HERE=Path(__file__).resolve().parent

def ensure(ok,msg):
    if not ok:raise ValueError(msg)
def make_auth(report,n=1):
    policy={'version':'single-use-v1','action':'export_report','scope':'demo_directory','export_enabled':True}
    auth={'authorization_id':'demo-auth-%03d'%n,'action':'export_report','destination':'approved/report-%03d.txt'%n,'scope':'demo_directory','policy_sha256':sha(canonical(policy)),'report_sha256':sha(report),'issued_at':2000000000000,'expires_at':2000000001000}
    return {'authorization':auth,'policy':policy,'report':report.decode(),'time':2000000000500}
def inventory(root):
    result={}
    for p in Path(root).rglob('*'):
        if p.is_symlink():raise ValueError('SYMLINK_EXPORT')
        if p.is_file():result[p.relative_to(root).as_posix()]=sha(p.read_bytes())
    return result

def suite(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    report=(HERE/'report.txt').read_bytes();base=make_auth(report);records=[]
    with tempfile.TemporaryDirectory(prefix='di2-single-use-') as tmp:
        temp=Path(tmp)
        def scenario(name,requests=None):
            root=temp/name
            init_store(root,[r['authorization'] for r in (requests or [base])])
            return root,{'id':name,'workers':[],'initial_snapshot':snapshot(root)}
        def spawn(root,rec,request,name,barrier=None,crash=None):
            f=root/(name+'.request.json');save(f,request)
            p=subprocess.Popen([sys.executable,'-B',str(HERE/'worker.py'),str(root),str(f),name,str(barrier) if barrier else '-',crash or ''],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            return p,{'worker':name,'pid':p.pid,'request':request}
        def finish(p,w):
            try:stdout,stderr=p.communicate(timeout=20)
            except subprocess.TimeoutExpired:p.kill();p.communicate();raise ValueError('WORKER_TIMEOUT')
            ensure(p.returncode==0 and not stderr,'WORKER_FAILED')
            w.update(exit_code=p.returncode,result=json.loads(stdout));return w
        def call(root,rec,req,name):
            p,w=spawn(root,rec,req,name);w=finish(p,w);rec['workers'].append(w);return w['result']
        def end(root,rec,valid=True):
            rec['final_snapshot']=snapshot(root) if valid else None
            rec['exports']=inventory(root/'exports')
            dest=out/rec['id'];dest.mkdir()
            if rec['exports']:shutil.copytree(root/'exports',dest/'exports')
            save(dest/'case.json',rec);records.append(rec)
        root,r=scenario('baseline_and_reuse')
        first=call(root,r,base,'first');ensure(first['outcome']=='COMPLETED','BASELINE')
        target=root/'exports'/base['authorization']['destination'];inode=target.stat().st_ino
        duplicate=call(root,r,base,'duplicate');ensure(duplicate['outcome']=='ALREADY_COMPLETED' and duplicate['write_open_attempts']==0,'DUPLICATE')
        ensure(inode==target.stat().st_ino,'DUPLICATE_REPLACED_FILE')
        r['same_inode_after_retry']=True;end(root,r)
        baseline_root=root;baseline_snapshot=snapshot(root);baseline_exports=inventory(root/'exports')

        root,r=scenario('twenty_processes')
        control=root/'control';control.mkdir();go=control/'GO'
        procs=[spawn(root,r,base,'worker_%02d'%i,go) for i in range(20)]
        try:
            deadline=time.monotonic()+10
            while len(list(control.glob('*.ready')))<20:
                ensure(time.monotonic()<deadline,'READY_TIMEOUT');time.sleep(.005)
            r['all_workers_ready_before_release']=True
            go.write_text('go\n')
            r['workers']=[finish(p,w) for p,w in procs]
        finally:
            for p,w in procs:
                if p.poll() is None:p.kill();p.communicate()
        ensure(len({w['pid'] for w in r['workers']})==20,'NOT_SEPARATE_PROCESSES')
        ensure(sum(w['result']['outcome']=='COMPLETED' for w in r['workers'])==1,'COMPETING_COMPLETIONS')
        ensure(sum(w['result']['outcome']=='ALREADY_COMPLETED' for w in r['workers'])==19,'UNACCOUNTED_COMPETITOR')
        ensure(sum(w['result']['write_open_attempts'] for w in r['workers'])==1,'DUPLICATE_OPEN')
        end(root,r)

        second=make_auth(report,2);root,r=scenario('two_authorizations',[base,second])
        ensure(call(root,r,base,'one')['outcome']=='COMPLETED','TWO_FIRST')
        ensure(call(root,r,second,'two')['outcome']=='COMPLETED','TWO_SECOND');end(root,r)

        for name in ('changed_content','changed_destination','expired','changed_policy'):
            root,r=scenario(name);q=copy.deepcopy(base)
            if name=='changed_content':q['report']+='Altered.\n';q['authorization']['report_sha256']=sha(q['report'].encode())
            elif name=='changed_destination':q['authorization']['destination']='approved/report-099.txt'
            elif name=='expired':q['time']=q['authorization']['expires_at']
            else:q['policy']['export_enabled']=False
            result=call(root,r,q,'refused');ensure(result['outcome']=='REFUSED' and result['write_open_attempts']==0,'INVALID_REQUEST_EXPORTED');end(root,r)

        for name in ('missing_store','malformed_schema','corrupted_store','missing_authorization_row'):
            root,r=scenario(name);dbpath=root/'state.sqlite'
            if name=='missing_store':dbpath.unlink()
            elif name=='corrupted_store':dbpath.write_bytes(b'not a SQLite database\n')
            else:
                with sqlite3.connect(dbpath) as db:
                    db.execute('DROP TABLE metadata' if name=='malformed_schema' else 'DELETE FROM authorizations')
            before=sha(dbpath.read_bytes()) if dbpath.exists() else None
            r['fault']=name;r['fault_state_hash_before']=before
            result=call(root,r,base,'refused')
            after=sha(dbpath.read_bytes()) if dbpath.exists() else None
            ensure(result['outcome']=='REFUSED' and result['write_open_attempts']==0 and before==after,'BAD_STATE_RESET_OR_EXPORT')
            r['fault_state_hash_after']=after;end(root,r,False)

        for point in ('after_reservation','after_file','after_completion'):
            root,r=scenario('crash_'+point)
            p,w=spawn(root,r,base,'crashed',crash=point)
            try:
                checkpoint=root/'crashed.checkpoint.json';deadline=time.monotonic()+10
                while not checkpoint.exists():
                    ensure(p.poll() is None and time.monotonic()<deadline,'CRASH_POINT_NOT_REACHED');time.sleep(.005)
                r['checkpoint']=load(checkpoint)
                # SIGKILL only the Popen handle created for this scenario.
                p.kill();stdout,stderr=p.communicate(timeout=5)
                ensure(p.returncode==-signal.SIGKILL,'NOT_SIGKILL')
                ensure(not stdout,'UNEXPECTED_PRECRASH_ACK')
                w.update(exit_code=p.returncode,result=None);r['workers'].append(w)
            finally:
                if p.poll() is None:p.kill();p.communicate()
            r['snapshot_after_kill']=snapshot(root);r['exports_after_kill']=inventory(root/'exports')
            target=root/'exports'/base['authorization']['destination']
            inode=target.stat().st_ino if target.exists() else None
            got=call(root,r,base,'recovery')
            expected='ALREADY_COMPLETED' if point=='after_completion' else 'UNCERTAIN'
            ensure(got['outcome']==expected and got['write_open_attempts']==0,'BAD_RECOVERY')
            got2=call(root,r,base,'retry_again')
            ensure(got2['write_open_attempts']==0,'RECOVERY_RETRY_WRITE')
            ensure(inventory(root/'exports')==r['exports_after_kill'],'RECOVERY_CHANGED_EXPORTS')
            ensure((target.stat().st_ino if target.exists() else None)==inode,'RECOVERY_REPLACED_FILE')
            r['same_inode_after_recovery']=True;end(root,r)
        ensure(snapshot(baseline_root)==baseline_snapshot and inventory(baseline_root/'exports')==baseline_exports,'BASELINE_CHANGED')
    summary={'status':'PASS','scenario_count':len(records),'competing_processes':20,'sigkill_cases':3,'baseline_unchanged':True,'execution_boundary':'isolated local harness, cooperative processes','outcomes':{r['id']:[w['result']['outcome'] if w['result'] else 'SIGKILL_NO_ACK' for w in r['workers']] for r in records}}
    save(out/'suite-results.json',summary);return summary
if __name__=='__main__':
    try:print(json.dumps(suite(sys.argv[1]),indent=2))
    except Exception as e:print(json.dumps({'status':'FAIL','reason':str(e)}));sys.exit(1)
