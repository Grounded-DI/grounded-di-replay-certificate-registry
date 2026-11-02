import pathlib,tempfile,json,copy,subprocess,sys,hashlib
from fractions import Fraction
P=pathlib.Path(__file__).resolve().parent; E=lambda x:(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode();s0=json.loads((P/'source_record.json').read_text());f0=json.loads((P/'fixture.json').read_text());names=['changed_coefficient','outside_range','reversed_bounds','missing_bound','celsius','kilojoules','valid_input_change','altered_intermediate','wrong_result_rehashed'];rows=[]
for name in names:
 with tempfile.TemporaryDirectory() as tmp:
  p=pathlib.Path(tmp);s=copy.deepcopy(s0);f=copy.deepcopy(f0);out=p/'out'
  if name=='changed_coefficient':s['coefficients']['A']='-203.6061';change='A changed after freeze'
  elif name=='outside_range':f['temperature_end']='501';change='end temperature 501 K'
  elif name=='reversed_bounds':f['temperature_start']='300';f['temperature_end']='298';change='reverse bounds'
  elif name=='missing_bound':del f['temperature_end'];change='remove upper bound'
  elif name=='celsius':f['temperature_unit']='C';change='set unit C without conversion'
  elif name=='kilojoules':f['energy_unit']='kJ';change='set energy unit kJ without conversion'
  elif name=='valid_input_change':f['amount_mol']='2';change='double amount to 2 mol'
  elif name=='altered_intermediate':change='alter Cp endpoint record before integral'
  else:change='replace final heat with zero and recompute commitment'
  sp=p/'source.json';fp=p/'fixture.json';sp.write_bytes(E(s));fp.write_bytes(E(f));args=[sys.executable,'-B',str(P/'pipeline.py'),'--source',str(sp),'--fixture',str(fp),'--out',str(out)]
  if name=='altered_intermediate':hand=p/'handoff.json';hand.write_bytes(E({'cp_start_J_per_mol_K':'0','cp_end_J_per_mol_K':'0'}));args+=['--handoff',str(hand)]
  r=subprocess.run(args,capture_output=True,text=True);result=json.loads(r.stdout) if r.stdout else {};check=None;ok=False
  if name=='valid_input_change' and r.returncode==0:
   v=subprocess.run([sys.executable,'-B',str(P/'checker.py'),'--source',str(sp),'--fixture',str(fp),'--out',str(out)],capture_output=True,text=True);check={'exit':v.returncode,'stdout':v.stdout,'stderr':v.stderr};j=json.loads(v.stdout) if v.stdout else {};base=Fraction(json.loads((P/'CONTRACT.json').read_text())['expected_exact']['integrated_J']);ok=Fraction(result['heat_J'])==2*base and v.returncode==1 and j.get('math') and not j.get('frozen_bindings')
  elif name=='wrong_result_rehashed' and r.returncode==0:
   z=out/'05_integral.json';obj=json.loads(z.read_text());obj['heat_J']='0';z.write_bytes(E(obj));m=out/'07_commitment.json';j=json.loads(m.read_text());j['artifacts'][z.name]=hashlib.sha256(z.read_bytes()).hexdigest();m.write_bytes(E(j));v=subprocess.run([sys.executable,'-B',str(P/'checker.py'),'--source',str(sp),'--fixture',str(fp),'--out',str(out)],capture_output=True,text=True);check={'exit':v.returncode,'stdout':v.stdout,'stderr':v.stderr};result=json.loads(v.stdout) if v.stdout else {};ok=v.returncode==1 and result.get('commitment_consistent') and not result.get('math') and not result.get('hashes')
  else:
   reason={'changed_coefficient':'SOURCE_IDENTITY','outside_range':'RANGE','reversed_bounds':'RANGE','missing_bound':'SCHEMA','celsius':'UNIT','kilojoules':'UNIT','altered_intermediate':'HANDOFF'}.get(name);ok=r.returncode==2 and result.get('status')=='REJECT' and result.get('reason')==reason and not out.exists()
  rows.append({'case':name,'change':change,'expected':'valid new doubled result, baseline checker rejects' if name=='valid_input_change' else ('consistent commitment but checker rejects' if name=='wrong_result_rehashed' else 'controlled rejection before output'),'actual':result,'pipeline_exit':r.returncode,'pipeline_stdout':r.stdout,'pipeline_stderr':r.stderr,'checker':check,'assertion':'PASS' if ok else 'FAIL'})
  if not ok:print(json.dumps({'status':'FAIL','records':rows},indent=2));sys.exit(1)
print(json.dumps({'status':'PASS','registered':9,'executed':9,'passed':9,'failed':0,'errors':0,'skipped':0,'records':rows},indent=2))
