"""Single-use local demo gate. Cooperative processes only; no installed-app gate."""
import contextlib,fcntl,json,os,re,signal,sqlite3,time
from pathlib import Path
from codec import canonical,sha,load,save
STATES={'UNUSED','RESERVED','COMPLETED','UNCERTAIN'}

def append(db,kind,auth,old,new,worker,when,detail=None):
    last=db.execute('SELECT seq,hash FROM events ORDER BY seq DESC LIMIT 1').fetchone()
    event={'seq':last[0]+1 if last else 1,'previous':last[1] if last else '0'*64,'kind':kind,'authorization_id':auth['authorization_id'],'authorization_sha256':sha(canonical(auth)),'from':old,'to':new,'worker':worker,'time':when,'detail':detail}
    encoded=canonical(event);db.execute('INSERT INTO events VALUES (?,?,?)',(event['seq'],encoded.decode(),sha(encoded)))

def init_store(root,authorizations):
    root=Path(root);root.mkdir(mode=0o700,parents=True,exist_ok=False)
    if len({a['authorization_id'] for a in authorizations})!=len(authorizations):raise ValueError('DUPLICATE_ENROLLMENT')
    for a in authorizations:
        if not valid_auth(a):raise ValueError('INVALID_ENROLLMENT')
    save(root/'enrollment.json',authorizations)
    with (root/'enrollment.json').open('rb') as f:os.fsync(f.fileno())
    db=sqlite3.connect(root/'state.sqlite',isolation_level=None)
    try:
        db.execute('PRAGMA journal_mode=DELETE');db.execute('PRAGMA synchronous=FULL')
        db.executescript('CREATE TABLE metadata(version INTEGER NOT NULL); INSERT INTO metadata VALUES(1); CREATE TABLE authorizations(id TEXT PRIMARY KEY,body TEXT NOT NULL,state TEXT NOT NULL); CREATE TABLE events(seq INTEGER PRIMARY KEY,body TEXT NOT NULL,hash TEXT NOT NULL);')
        db.execute('BEGIN IMMEDIATE')
        for a in authorizations:
            db.execute('INSERT INTO authorizations VALUES (?,?,?)',(a['authorization_id'],canonical(a).decode(),'UNUSED'))
            append(db,'ENROLLED',a,None,'UNUSED','initializer',a['issued_at'])
        db.commit()
    finally:db.close()
    (root/'exports').mkdir(mode=0o700)
    fd=os.open(root,os.O_RDONLY|os.O_DIRECTORY);os.fsync(fd);os.close(fd)

def valid_auth(a):
    keys={'authorization_id','report_sha256','destination','action','policy_sha256','scope','issued_at','expires_at'}
    return type(a) is dict and set(a)==keys and bool(re.fullmatch(r'demo-auth-[0-9]{3}',str(a['authorization_id']))) and type(a['destination']) is str and bool(re.fullmatch(r'approved/report-[0-9]{3}\.txt',a['destination'])) and a['action']=='export_report' and a['scope']=='demo_directory' and all(type(a[k]) is str and re.fullmatch('[a-f0-9]{64}',a[k]) for k in ('report_sha256','policy_sha256')) and all(type(a[k]) is int and 0<=a[k]<=9007199254740991 for k in ('issued_at','expires_at')) and a['issued_at']<a['expires_at']

@contextlib.contextmanager
def lock(root):
    root=Path(root)
    if root.is_symlink() or not root.is_dir():raise ValueError('STATE_MISSING')
    fd=os.open(root/'gate.lock',os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
    try:
        deadline=time.monotonic()+10
        while True:
            try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);break
            except BlockingIOError:
                if time.monotonic()>deadline:raise ValueError('LOCK_TIMEOUT')
                time.sleep(.005)
        yield
    finally:os.close(fd)

def open_valid(root):
    root=Path(root)
    for name in ('enrollment.json','state.sqlite'):
        p=root/name
        if p.is_symlink() or not p.is_file():raise ValueError('STATE_MISSING')
    enrolled=load(root/'enrollment.json')
    if type(enrolled) is not list or not enrolled or not all(valid_auth(a) for a in enrolled):raise ValueError('ENROLLMENT_INVALID')
    db=sqlite3.connect((root/'state.sqlite').resolve().as_uri()+'?mode=rw',uri=True,timeout=5,isolation_level=None)
    try:
        db.execute('PRAGMA synchronous=FULL')
        if db.execute('PRAGMA integrity_check').fetchall()!=[('ok',)]:raise ValueError('STATE_CORRUPT')
        if db.execute('SELECT version FROM metadata').fetchall()!=[(1,)]:raise ValueError('STATE_SCHEMA_INVALID')
        expected={a['authorization_id']:a for a in enrolled}
        if len(expected)!=len(enrolled):raise ValueError('ENROLLMENT_INVALID')
        rows={i:(json.loads(b),s) for i,b,s in db.execute('SELECT id,body,state FROM authorizations')}
        if set(rows)!=set(expected):raise ValueError('STATE_ENROLLMENT_MISMATCH')
        for i,(a,s) in rows.items():
            if canonical(a)!=canonical(expected[i]) or s not in STATES:raise ValueError('STATE_BINDING_MISMATCH')
        states={};prev='0'*64
        for n,(seq,body,h) in enumerate(db.execute('SELECT seq,body,hash FROM events ORDER BY seq'),1):
            e=json.loads(body);i=e['authorization_id']
            if seq!=n or e['seq']!=n or e['previous']!=prev or sha(canonical(e))!=h or i not in expected or e['authorization_sha256']!=sha(canonical(expected[i])):raise ValueError('EVENT_INTEGRITY')
            if e['from']!=states.get(i):raise ValueError('EVENT_STATE')
            transition=(e['kind'],e['from'],e['to'])
            allowed=transition in [('ENROLLED',None,'UNUSED'),('RESERVED','UNUSED','RESERVED'),('COMPLETED','RESERVED','COMPLETED'),('UNCERTAIN','RESERVED','UNCERTAIN')]
            if not allowed and not(e['kind']=='REFUSED' and e['to']==e['from'] and e['from'] in STATES):raise ValueError('EVENT_TRANSITION')
            states[i]=e['to'];prev=h
        if states!={i:s for i,(a,s) in rows.items()}:raise ValueError('STATE_HISTORY_MISMATCH')
        return db,expected
    except BaseException:
        db.close();raise

def checkpoint(root,worker,point,requested):
    if point!=requested:return
    save(Path(root)/(worker+'.checkpoint.json'),{'worker':worker,'point':point})
    # Test runner SIGKILLs only this owned process after observing its checkpoint.
    os.kill(os.getpid(),signal.SIGSTOP)
    raise RuntimeError('CRASH_CHECKPOINT_RESUMED_UNEXPECTEDLY')

def handle(root,request,worker,crash=None):
    root=Path(root)
    result={'worker':worker,'outcome':'REFUSED','reason':None,'write_open_attempts':0}
    try:
        with lock(root):
            db,enrolled=open_valid(root)
            try:
                supplied=request.get('authorization');when=request.get('time');policy=request.get('policy');report=request.get('report','').encode('utf-8')
                if not valid_auth(supplied):raise ValueError('AUTHORIZATION_INVALID')
                a=enrolled.get(supplied['authorization_id'])
                if a is None:raise ValueError('AUTHORIZATION_NOT_ENROLLED')
                state=db.execute('SELECT state FROM authorizations WHERE id=?',(a['authorization_id'],)).fetchone()[0]
                def refuse(reason):
                    db.execute('BEGIN IMMEDIATE');append(db,'REFUSED',a,state,state,worker,when,{'reason':reason});db.commit()
                    result['reason']=reason;return result
                if canonical(a)!=canonical(supplied):return refuse('AUTHORIZATION_BINDING_MISMATCH')
                if sha(report)!=a['report_sha256']:return refuse('REPORT_HASH_MISMATCH')
                if type(policy) is not dict or sha(canonical(policy))!=a['policy_sha256']:return refuse('POLICY_HASH_MISMATCH')
                if policy!={'version':'single-use-v1','action':'export_report','scope':'demo_directory','export_enabled':True}:return refuse('POLICY_UNSUPPORTED')
                if type(when) is not int or not a['issued_at']<=when<a['expires_at']:return refuse('TIME_INVALID_OR_EXPIRED')
                target=root/'exports'/a['destination']
                if state=='RESERVED':
                    observed=sha(target.read_bytes()) if target.is_file() and not target.is_symlink() else None
                    db.execute('BEGIN IMMEDIATE');db.execute('UPDATE authorizations SET state=? WHERE id=?',('UNCERTAIN',a['authorization_id']));append(db,'UNCERTAIN',a,'RESERVED','UNCERTAIN',worker,when,{'observed_report_sha256':observed,'reason':'RESERVATION_WITHOUT_COMPLETION'});db.commit()
                    return dict(result,outcome='UNCERTAIN',reason='RESERVATION_WITHOUT_COMPLETION')
                if state=='UNCERTAIN':return refuse('UNCERTAIN_NO_RETRY')
                if state=='COMPLETED':
                    if target.is_symlink() or not target.is_file() or sha(target.read_bytes())!=a['report_sha256']:return refuse('COMPLETED_ARTIFACT_INVALID')
                    refuse('ALREADY_COMPLETED');return dict(result,outcome='ALREADY_COMPLETED')
                db.execute('BEGIN IMMEDIATE');db.execute('UPDATE authorizations SET state=? WHERE id=?',('RESERVED',a['authorization_id']));append(db,'RESERVED',a,'UNUSED','RESERVED',worker,when);db.commit()
                checkpoint(root,worker,'after_reservation',crash)
                # Write only in the pinned local output directory using a validated leaf name.
                dfd=os.open(root/'exports',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
                try:
                    try:os.mkdir('approved',0o700,dir_fd=dfd)
                    except FileExistsError:pass
                    afd=os.open('approved',os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=dfd)
                    try:
                        result['write_open_attempts']=1
                        fd=os.open(a['destination'].split('/')[1],os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=afd)
                        with os.fdopen(fd,'wb') as f:f.write(report);f.flush();os.fsync(f.fileno())
                        os.fsync(afd)
                    finally:os.close(afd)
                    os.fsync(dfd)
                finally:os.close(dfd)
                checkpoint(root,worker,'after_file',crash)
                db.execute('BEGIN IMMEDIATE');db.execute('UPDATE authorizations SET state=? WHERE id=?',('COMPLETED',a['authorization_id']));append(db,'COMPLETED',a,'RESERVED','COMPLETED',worker,when,{'report_sha256':sha(report)});db.commit()
                checkpoint(root,worker,'after_completion',crash)
                return dict(result,outcome='COMPLETED',reason='EXPORTED')
            finally:db.close()
    except Exception as e:
        # Do not expose paths or silently rebuild bad state. Any reservation survives.
        reason=str(e) if isinstance(e,ValueError) else type(e).__name__
        return dict(result,reason=reason)

def snapshot(root):
    with lock(root):
        db,enrolled=open_valid(root)
        try:return {'enrollment':list(enrolled.values()),'states':{i:s for i,s in db.execute('SELECT id,state FROM authorizations')},'events':[{'event':json.loads(b),'sha256':h} for b,h in db.execute('SELECT body,hash FROM events ORDER BY seq')]}
        finally:db.close()
