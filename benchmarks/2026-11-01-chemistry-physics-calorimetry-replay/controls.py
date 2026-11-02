import pathlib,subprocess,tempfile,json,sys,copy,hashlib
P=pathlib.Path(__file__).resolve().parent
encode=lambda x:(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
base=json.loads((P/'fixture.json').read_text()); names=['changed_amount','changed_energy','unit_swap','capture_outside_range','zero_mass','zero_heat_capacity','missing_unit','altered_chemistry_handoff','coherent_wrong_temperature_rehashed'];records=[]
for name in names:
 with tempfile.TemporaryDirectory() as temp:
  d=copy.deepcopy(base);p=pathlib.Path(temp);out=p/'out';change='';target=None
  if name=='changed_amount':d['material_amount']['value']='3';change='amount 2 -> 3 mol';target='15/4'
  elif name=='changed_energy':d['energy_per_mole']['value']='20';change='energy 40 -> 20 kJ/mol';target='5/4'
  elif name=='unit_swap':d['energy_per_mole']['unit']='J/mol';change='unit kJ/mol -> J/mol without converting value'
  elif name=='capture_outside_range':d['capture_fraction']['value']='3/2';change='capture fraction -> 3/2'
  elif name=='zero_mass':d['water_mass']['value']='0';change='water mass -> 0 kg'
  elif name=='zero_heat_capacity':d['heat_capacity']['value']='0';change='heat capacity -> 0 J/(kg*K)'
  elif name=='missing_unit':del d['water_mass']['unit'];change='water mass unit removed'
  elif name=='altered_chemistry_handoff':change='chemistry output modified from 80000 J to 80001 J'
  else:change='temperature changed to zero and commitment recomputed'
  f=p/'fixture.json';f.write_bytes(encode(d));cmd=[sys.executable,'-B',str(P/'pipeline.py'),'--fixture',str(f),'--out',str(out)];
  if name=='altered_chemistry_handoff':
   hand=p/'handoff.json';hand.write_bytes(encode({'energy_release':{'value':'80001','unit':'J'}}));cmd+=['--handoff',str(hand)]
  r=subprocess.run(cmd,capture_output=True,text=True);checker=None;actual={};assertion=False
  if name in ('changed_amount','changed_energy'):
   assert r.returncode==0; actual=json.loads(r.stdout);v=subprocess.run([sys.executable,'-B',str(P/'checker.py'),'--fixture',str(f),'--out',str(out)],capture_output=True,text=True);checker={'exit':v.returncode,'stdout':v.stdout,'stderr':v.stderr};assertion=actual['temperature_change_K']==target and v.returncode==1 and json.loads(v.stdout)['status']=='REJECT'
  elif name=='coherent_wrong_temperature_rehashed':
   assert r.returncode==0;path=out/'05_temperature.json';path.write_bytes(encode({'temperature_change':{'value':'0','unit':'K'}}));c=json.loads((out/'07_commitment.json').read_text());c['artifacts'][path.name]=hashlib.sha256(path.read_bytes()).hexdigest();(out/'07_commitment.json').write_bytes(encode(c));v=subprocess.run([sys.executable,'-B',str(P/'checker.py'),'--fixture',str(f),'--out',str(out)],capture_output=True,text=True);checker={'exit':v.returncode,'stdout':v.stdout,'stderr':v.stderr};actual=json.loads(v.stdout);assertion=v.returncode==1 and actual['commitment_consistent'] and not actual['math'] and not actual['hashes']
  else:
   try:actual=json.loads(r.stdout)
   except json.JSONDecodeError:actual={'status':'HARNESS_ERROR'}
   reason={'unit_swap':'UNIT_OR_SCHEMA','capture_outside_range':'CAPTURE_RANGE','zero_mass':'NONPOSITIVE_DENOMINATOR','zero_heat_capacity':'NONPOSITIVE_DENOMINATOR','missing_unit':'UNIT_OR_SCHEMA','altered_chemistry_handoff':'CHEMISTRY_HANDOFF_MISMATCH'}[name];assertion=r.returncode==2 and actual.get('status')=='REJECT' and actual.get('reason')==reason and not out.exists()
  records.append({'name':name,'change':change,'expected':target+' K and verifier REJECT' if target else ('consistent commitment, math and frozen checks REJECT' if name=='coherent_wrong_temperature_rehashed' else 'controlled REJECT, no output'),'actual':actual,'pipeline_exit':r.returncode,'pipeline_stdout':r.stdout,'pipeline_stderr':r.stderr,'checker':checker,'assertion':'PASS' if assertion else 'FAIL'})
  if not assertion:print(json.dumps({'status':'FAIL','records':records},indent=2));sys.exit(1)
print(json.dumps({'status':'PASS','registered':len(names),'executed':len(records),'passed':sum(x['assertion']=='PASS' for x in records),'failed':0,'errors':0,'skipped':0,'records':records},indent=2))
