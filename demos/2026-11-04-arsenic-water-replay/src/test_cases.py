import sys,pathlib,subprocess,json,hashlib,copy,tempfile,shutil,platform
R=pathlib.Path(__file__).resolve().parents[1];P=R/'src/producer.py';C=R/'src/checker.py';fixture=R/'frozen/fixture.json';base=R/'evidence/run1';other=R/'evidence/run2';tmp=pathlib.Path(tempfile.mkdtemp(prefix='water_replay_'));f=json.loads(fixture.read_text());cases=[]
def state(p):
 if not p.exists():return 'ABSENT'
 return {str(x.relative_to(p)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(p.rglob('*')) if x.is_file()}
def run(name,script,inp,out,expected,check=None,unchanged=False):
 before=state(out);cmd=[sys.executable,'-B',str(script),str(inp),str(out)];p=subprocess.run(cmd,capture_output=True,text=True);after=state(out)
 try:s=json.loads(p.stdout)['status']
 except Exception:s='NO_STATUS'
 actual={'exit':p.returncode,'status':s,'stdout':p.stdout,'stderr':p.stderr}
 ok=(p.returncode,s)==tuple(expected) and (not unchanged or before==after)
 if check and p.returncode==0:
  rows=json.loads((out/'04_comparison.json').read_text());row=next(x for x in rows if x['id']=='A');actual['claim_A']=[row['comparison'],row['reason']];ok &= actual['claim_A']==check
 cases.append({'name':name,'change':name,'command':cmd,'expected':{'exit':expected[0],'status':expected[1],'sample_A':check,'unchanged':unchanged},'actual':actual,'before':before,'after':after,'result':'PASS' if ok else 'FAIL'})
def write(name,d):p=tmp/(name+'.json');p.write_text(json.dumps(d)+'\n');return p
def mutate(name,fn,expected,check=None):
 d=copy.deepcopy(f);fn(d);p=write(name,d);run(name,P,p,tmp/(name+'_out'),expected,check)
for n in sorted(x.name for x in base.iterdir()):
 a=(base/n).read_bytes();b=(other/n).read_bytes();cases.append({'name':'replay_'+n,'expected':'identical bytes','actual':{'bytes_equal':a==b,'sha256_a':hashlib.sha256(a).hexdigest(),'sha256_b':hashlib.sha256(b).hexdigest()},'before':'N/A','after':'N/A','result':'PASS' if a==b else 'FAIL'})
run('checker_run1',C,fixture,base,(0,'OK'),unchanged=True);run('checker_run2',C,fixture,other,(0,'OK'),unchanged=True)
expected={'A':['BELOW','NUMERIC_COMPARISON'],'B':['ABOVE','NUMERIC_COMPARISON'],'C':['HOLD','BELOW_REPORTING_LIMIT'],'D':['EQUAL','NUMERIC_COMPARISON'],'E':['BELOW','NUMERIC_COMPARISON'],'F':['ABOVE','NUMERIC_COMPARISON'],'G':['HOLD','CONTEXT_OUT_OF_SCOPE']};actual={x['id']:[x['comparison'],x['reason']] for x in json.loads((base/'04_comparison.json').read_text())};cases.append({'name':'manual_fixture','expected':expected,'actual':actual,'before':'N/A','after':'N/A','result':'PASS' if expected==actual else 'FAIL'})
mutate('missing_source',lambda d:d.pop('source'),(2,'INVALID_SOURCE'))
mutate('changed_source',lambda d:d['source'].__setitem__('threshold','11'),(2,'INVALID_SOURCE'))
mutate('missing_unit',lambda d:d['samples'][0].pop('unit'),(2,'INVALID_INPUT'))
mutate('unsupported_unit',lambda d:d['samples'][0].__setitem__('unit','ppm'),(0,'OK'),['HOLD','UNIT_UNSUPPORTED'])
mutate('boundary_equal',lambda d:d['samples'][0].__setitem__('result','10'),(0,'OK'),['EQUAL','NUMERIC_COMPARISON'])
mutate('boundary_below',lambda d:d['samples'][0].__setitem__('result','9.999'),(0,'OK'),['BELOW','NUMERIC_COMPARISON'])
mutate('boundary_above',lambda d:d['samples'][0].__setitem__('result','10.001'),(0,'OK'),['ABOVE','NUMERIC_COMPARISON'])
mutate('below_reporting_limit',lambda d:d['samples'][0].update({'status':'below_limit','result':None}),(0,'OK'),['HOLD','BELOW_REPORTING_LIMIT'])
mutate('out_of_scope',lambda d:d['samples'][0].__setitem__('context','raw_water'),(0,'OK'),['HOLD','CONTEXT_OUT_OF_SCOPE'])
mutate('inconsistent',lambda d:d['samples'][0].update({'result':'0.1','reporting_limit':'1'}),(0,'OK'),['HOLD','INCONSISTENT_RESULT'])
d=copy.deepcopy(f);d['samples'][0]['result']='9';changed=write('changed_input',d);run('changed_after_generation',C,changed,base,(1,'CHECK_FAILED'),unchanged=True)
d=copy.deepcopy(f);d['source']['id']='other';s=write('bad_source_checker',d);run('changed_source_checker',C,s,base,(2,'INVALID_SOURCE'),unchanged=True)
for typ in ['missing','malformed','altered','coherent_artifact_forgery']:
 out=tmp/typ;shutil.copytree(base,out);p=out/'04_comparison.json'
 if typ=='missing':p.unlink()
 elif typ=='malformed':p.write_text('{')
 else:
  v=json.loads(p.read_text());v[0]['comparison']='ABOVE';p.write_text(json.dumps(v,sort_keys=True,separators=(',',':'))+'\n')
  if typ=='coherent_artifact_forgery':
   report=out/'05_report.json';z=json.loads(report.read_text());z['results']=v;report.write_text(json.dumps(z,sort_keys=True,separators=(',',':'))+'\n');commit={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(out.iterdir()) if x.name!='06_commitment.json'};(out/'06_commitment.json').write_text(json.dumps(commit,sort_keys=True,separators=(',',':'))+'\n')
 run(typ+'_artifact',C,fixture,out,(1,'CHECK_FAILED'),unchanged=True)
run('existing_destination',P,fixture,base,(2,'OUTPUT_EXISTS'),unchanged=True)
new=tmp/'coherent_input_output';run('changed_input_regenerated_producer',P,changed,new,(0,'OK'),['BELOW','NUMERIC_COMPARISON']);run('changed_input_regenerated_checker',C,changed,new,(0,'OK'),unchanged=True)
summary={'total':len(cases),'passed':sum(c['result']=='PASS' for c in cases),'failed':sum(c['result']=='FAIL' for c in cases),'errors':0,'skips':0,'python':sys.version,'platform':platform.platform(),'cases':cases};(R/'evidence/test_results.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='cases'},indent=2));sys.exit(bool(summary['failed']))
