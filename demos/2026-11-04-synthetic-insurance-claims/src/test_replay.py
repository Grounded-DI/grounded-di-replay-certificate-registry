import json,pathlib,subprocess,sys,hashlib,shutil,copy,tempfile,platform,os
ROOT=pathlib.Path(__file__).resolve().parents[1]; P=ROOT/'src/producer.py';C=ROOT/'src/checker.py';F=ROOT/'frozen/fixture.json';BASE=ROOT/'evidence/run1';OUT=pathlib.Path(tempfile.mkdtemp(prefix='claims_replay_tests_'))
fixture=json.loads(F.read_text());results=[]
def digest_dir(path):
 if not path.exists():return 'ABSENT'
 return {str(x.relative_to(path)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(path.rglob('*')) if x.is_file()}
def invoke(script,inp,out):
 p=subprocess.run([sys.executable,'-B',str(script),str(inp),str(out)],capture_output=True,text=True)
 try:s=json.loads(p.stdout).get('status')
 except Exception:s='NO_STATUS'
 return p.returncode,s,p.stdout,p.stderr
def record(name,change,expect,actual,before,after,ok):results.append(dict(name=name,change=change,expected=expect,actual=actual,before=before,after=after,result='PASS' if ok else 'FAIL'))
def emit(name,data):
 f=OUT/(name+'.json');f.write_text(json.dumps(data),encoding='utf8');return f
def compare():
 a=ROOT/'evidence/run1';b=ROOT/'evidence/run2'
 for f in sorted(a.iterdir()):
  x=f.read_bytes();y=(b/f.name).read_bytes();record('replay_'+f.name,'fresh processes','bytes equal and SHA-256 equal',{'bytes_equal':x==y,'sha256_run1':hashlib.sha256(x).hexdigest(),'sha256_run2':hashlib.sha256(y).hexdigest()},digest_dir(a),digest_dir(b),x==y)
 for run in [a,b]:
  rc,s,so,se=invoke(C,F,run);h=digest_dir(run);record('check_'+run.name,'fresh process','OK / 0',{'exit':rc,'status':s,'stdout':so,'stderr':se},h,digest_dir(run),rc==0 and s=='OK' and h==digest_dir(run))
 expected={'A':['ROUTE_PAYMENT','COVERED_WITHIN_AUTHORITY',30000],'B':['HOLD','EVIDENCE_MISSING',0],'C':['DENY','EXCLUDED_CAUSE',0],'D':['ROUTE_PAYMENT','COVERED_WITHIN_AUTHORITY',50000],'E':['HOLD','AUTHORITY_EXCEEDED',0],'F':['HOLD','EVIDENCE_CONFLICT',0]}
 decisions=json.loads((a/'05_decisions.json').read_text());amounts={x['id']:x['amount'] for x in json.loads((a/'06_disposition.json').read_text())};got={x['id']:[x['decision'],x['reasons'][0],amounts[x['id']]] for x in decisions};record('hand_calculations','compare all six decisions','hand worksheet',got,'N/A','N/A',got==expected)
def invalid():
 malformed={'malformed':'{x','truncated':'{"policy":','duplicate_key':'{"policy":1,"policy":2}','float':F.read_text().replace('40000','40000.0',1),'boolean':F.read_text().replace('40000','true',1),'negative':F.read_text().replace('40000','-1',1),'bom':'\ufeff'+F.read_text(),'nan':F.read_text().replace('40000','NaN',1),'non_ascii':F.read_text().replace('"C1"','"é"',1)}
 d=copy.deepcopy(fixture);del d['policy'];malformed['missing_policy']=json.dumps(d)
 d=copy.deepcopy(fixture);del d['claims'][0]['amount'];malformed['missing_amount']=json.dumps(d)
 d=copy.deepcopy(fixture);d['claims'].append(copy.deepcopy(d['claims'][0]));malformed['duplicate_claim']=json.dumps(d)
 for name,content in malformed.items():
  path=OUT/(name+'.input');path.write_text(content,encoding='utf8');dest=OUT/('dest_'+name);before=digest_dir(dest);rc,s,so,se=invoke(P,path,dest);after=digest_dir(dest);record(name+'_producer',name,'INVALID_INPUT / 2; absent',{'exit':rc,'status':s,'stderr':se},before,after,(rc,s)==(2,'INVALID_INPUT') and before==after=='ABSENT')
  before=digest_dir(BASE);rc,s,so,se=invoke(C,path,BASE);after=digest_dir(BASE);record(name+'_checker',name,'INVALID_INPUT / 2; unchanged',{'exit':rc,'status':s,'stderr':se},before,after,(rc,s)==(2,'INVALID_INPUT') and before==after)
def case(name,change,expect):
 d=copy.deepcopy(fixture);change(d);path=emit(name,d);dest=OUT/('dest_'+name);before=digest_dir(dest);rc,s,so,se=invoke(P,path,dest);after=digest_dir(dest);ok=(rc,s)==(0,'OK')
 actual={'exit':rc,'status':s,'stderr':se}
 if ok:
  ds=json.loads((dest/'05_decisions.json').read_text());as_={x['id']:x['amount'] for x in json.loads((dest/'06_disposition.json').read_text())};i=next(x for x in ds if x['id']=='A');actual['A']=[i['decision'],i['reasons'][0],as_['A']];rr,ss,_,_=invoke(C,path,dest);actual['checker']=[rr,ss];ok=actual['A']==expect and (rr,ss)==(0,'OK')
 record(name,name,{'producer':[0,'OK'],'A':expect,'checker':[0,'OK']},actual,before,after,ok)
def scenarios():
 case('limit',lambda d:d['policy'].__setitem__('limit',10000),['ROUTE_PAYMENT','COVERED_WITHIN_AUTHORITY',10000])
 case('deductible',lambda d:d['policy'].__setitem__('deductible',40000),['HOLD','ZERO_AMOUNT',0])
 case('exclusion',lambda d:(d['policy'].__setitem__('covered',[]),d['policy']['excluded'].append('accidental_water')),['DENY','EXCLUDED_CAUSE',0])
 case('authority',lambda d:d['policy'].__setitem__('authority',29999),['HOLD','AUTHORITY_EXCEEDED',0])
 case('at_authority',lambda d:d['claims'][0].__setitem__('amount',60000),['ROUTE_PAYMENT','COVERED_WITHIN_AUTHORITY',50000])
 case('above_authority',lambda d:d['claims'][0].__setitem__('amount',60001),['HOLD','AUTHORITY_EXCEEDED',0])
 case('wrong_claim_binding',lambda d:d['claims'][0].__setitem__('claimant_id','C2'),['HOLD','BINDING_MISMATCH',0])
 case('wrong_evidence_policy',lambda d:d['claims'][0]['evidence'][0].__setitem__('policy_id','P2'),['HOLD','BINDING_MISMATCH',0])
 case('missing_evidence',lambda d:d['claims'][0].__setitem__('evidence',[]),['HOLD','EVIDENCE_MISSING',0])
 case('duplicate_evidence',lambda d:d['claims'][0]['evidence'].append(copy.deepcopy(d['claims'][0]['evidence'][0])),['HOLD','EVIDENCE_DUPLICATE',0])
 case('contradictory_evidence',lambda d:d['claims'][0]['evidence'][0].__setitem__('cause','intentional_damage'),['HOLD','EVIDENCE_CONFLICT',0])
def corruption():
 for name in ['missing','truncated','malformed','altered','coherent_forgery']:
  dest=OUT/('artifact_'+name);shutil.copytree(BASE,dest);target=dest/'05_decisions.json'
  if name=='missing':target.unlink()
  elif name=='truncated':target.write_bytes(target.read_bytes()[:10])
  elif name=='malformed':target.write_text('{')
  else:
   ds=json.loads(target.read_text());ds[0]['decision']='DENY';target.write_text(json.dumps(ds,sort_keys=True,separators=(',',':'))+'\n')
   if name=='coherent_forgery':
    dp=dest/'06_disposition.json';v=json.loads(dp.read_text());v[0]['disposition']='DENY';v[0]['amount']=0;dp.write_text(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n');commit={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(dest.iterdir()) if f.name!='07_commitment.json'};(dest/'07_commitment.json').write_text(json.dumps(commit,sort_keys=True,separators=(',',':'))+'\n')
  before=digest_dir(dest);rc,s,so,se=invoke(C,F,dest);after=digest_dir(dest);record(name+'_artifact',name,'CHECK_FAILED / 1; unchanged',{'exit':rc,'status':s,'stderr':se},before,after,(rc,s)==(1,'CHECK_FAILED') and before==after)
 d=copy.deepcopy(fixture);d['claims'][0]['amount']+=1;path=emit('changed_after',d);before=digest_dir(BASE);rc,s,so,se=invoke(C,path,BASE);after=digest_dir(BASE);record('input_changed_after','amount + 1','CHECK_FAILED / 1; unchanged',{'exit':rc,'status':s},before,after,(rc,s)==(1,'CHECK_FAILED') and before==after)
 before=digest_dir(BASE);rc,s,so,se=invoke(P,F,BASE);after=digest_dir(BASE);record('existing_destination_and_repeat','rerun against original run1','OUTPUT_EXISTS / 2; unchanged',{'exit':rc,'status':s},before,after,(rc,s)==(2,'OUTPUT_EXISTS') and before==after)
 d=copy.deepcopy(fixture);d['claims'].reverse();path=emit('reordered',d);dest=OUT/'dest_reordered';before=digest_dir(dest);rc,s,so,se=invoke(P,path,dest);after=digest_dir(dest);equal=digest_dir(BASE)==after;record('serialization_reordering','claims/key order and whitespace','OK / 0; all 7 bytes same',{'exit':rc,'status':s,'all_hashes_equal':equal},before,after,(rc,s)==(0,'OK') and equal)
compare();invalid();scenarios();corruption()
summary={'python':sys.version,'platform':platform.platform(),'total':len(results),'passed':sum(x['result']=='PASS' for x in results),'failed':sum(x['result']=='FAIL' for x in results),'errors':0,'skips':0,'cases':results}
(ROOT/'evidence/test_results.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='cases'},indent=2));sys.exit(1 if summary['failed'] else 0)
