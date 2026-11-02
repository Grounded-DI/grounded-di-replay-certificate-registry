import json,pathlib,subprocess,tempfile,copy,sys,hashlib
P=pathlib.Path(__file__).resolve().parent;encode=lambda x:(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode();base=json.loads((P/'fixture.json').read_text());source=json.loads((P/'source_record.json').read_text());names=['wrong_material','wrong_source_value','changed_conditions','missing_conditions','changed_unit','missing_source_reference','legitimate_input_change','altered_intermediate','coherent_wrong_result_rehashed'];records=[]
for name in names:
 with tempfile.TemporaryDirectory() as tmp:
  p=pathlib.Path(tmp);d=copy.deepcopy(base);s=copy.deepcopy(source);change=''
  if name=='wrong_material':d['material']='ethanol';change='material water -> ethanol'
  elif name=='wrong_source_value':s['property_value']='75.39';change='source Cp 75.38 -> 75.39'
  elif name=='changed_conditions':d['reference_temperature_K']='300';change='reference temperature 298 -> 300 K'
  elif name=='missing_conditions':del d['reference_temperature_K'];change='reference temperature removed'
  elif name=='changed_unit':d['heat_unit']='J';change='heat unit kJ -> J without conversion'
  elif name=='missing_source_reference':del d['source_sha256'];change='source binding removed'
  elif name=='legitimate_input_change':d['mass_g']='36.0306';change='mass doubled, expected delta 1/2 K'
  elif name=='altered_intermediate':change='quantity handoff changed from 1 to 2 mol'
  else:change='temperature changed to 0 K and manifest updated'
  sf=p/'source.json';ff=p/'fixture.json';sf.write_bytes(encode(s));ff.write_bytes(encode(d));out=p/'out';args=[sys.executable,'-B',str(P/'pipeline.py'),'--source',str(sf),'--fixture',str(ff),'--out',str(out)]
  if name=='altered_intermediate':
   hand=p/'handoff.json';hand.write_bytes(encode({'amount_mol':'2'}));args+=['--handoff',str(hand)]
  r=subprocess.run(args,capture_output=True,text=True);actual={};check=None;ok=False
  if name=='legitimate_input_change':
   if r.returncode==0:
    actual=json.loads(r.stdout);v=subprocess.run([sys.executable,'-B',str(P/'checker.py'),'--source',str(sf),'--fixture',str(ff),'--out',str(out)],capture_output=True,text=True);check={'exit':v.returncode,'stdout':v.stdout,'stderr':v.stderr};vr=json.loads(v.stdout) if v.stdout else {};ok=actual.get('temperature_change_K')=='1/2' and v.returncode==1 and vr.get('math') and not vr.get('fixture_frozen')
  elif name=='coherent_wrong_result_rehashed':
   if r.returncode==0:
    v=out/'05_result.json';x=json.loads(v.read_text());x['temperature_change_K']='0';v.write_bytes(encode(x));commit=out/'07_commitment.json';j=json.loads(commit.read_text());j['artifacts'][v.name]=hashlib.sha256(v.read_bytes()).hexdigest();commit.write_bytes(encode(j));w=subprocess.run([sys.executable,'-B',str(P/'checker.py'),'--source',str(sf),'--fixture',str(ff),'--out',str(out)],capture_output=True,text=True);check={'exit':w.returncode,'stdout':w.stdout,'stderr':w.stderr};actual=json.loads(w.stdout) if w.stdout else {};ok=w.returncode==1 and actual.get('commitment_consistent') and not actual.get('math') and not actual.get('hashes_match')
  else:
   try:actual=json.loads(r.stdout)
   except json.JSONDecodeError:actual={'status':'HARNESS_ERROR'}
   reason={'wrong_material':'MATERIAL_OR_CONDITIONS','wrong_source_value':'SOURCE_IDENTITY','changed_conditions':'MATERIAL_OR_CONDITIONS','missing_conditions':'MATERIAL_OR_CONDITIONS','changed_unit':'UNIT','missing_source_reference':'SOURCE_REFERENCE','altered_intermediate':'HANDOFF_MISMATCH'}[name];ok=r.returncode==2 and actual.get('reason')==reason and actual.get('status')=='REJECT' and not out.exists()
  records.append({'name':name,'change':change,'expected':'valid new result plus baseline verifier rejects' if name=='legitimate_input_change' else ('consistent commitment, verifier rejects bad result' if name=='coherent_wrong_result_rehashed' else 'controlled rejection before output'),'actual':actual,'pipeline_exit':r.returncode,'pipeline_stdout':r.stdout,'pipeline_stderr':r.stderr,'checker':check,'assertion':'PASS' if ok else 'FAIL'})
  if not ok:print(json.dumps({'status':'FAIL','records':records},indent=2));sys.exit(1)
print(json.dumps({'status':'PASS','registered':9,'executed':9,'passed':9,'failed':0,'errors':0,'skipped':0,'records':records},indent=2))
