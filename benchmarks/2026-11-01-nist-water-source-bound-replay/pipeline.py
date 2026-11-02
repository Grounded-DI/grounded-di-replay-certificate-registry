import argparse,json,hashlib,pathlib,sys
from fractions import Fraction as F
P=pathlib.Path(__file__).resolve().parent
encode=lambda x:(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode(); H=lambda b:hashlib.sha256(b).hexdigest()
N=['01_source.json','02_validation.json','03_normalized.json','04_quantity.json','05_result.json','06_assessment.json']
def run(source,fixture,out,handoff=None):
 c=json.loads((P/'CONTRACT.json').read_text());raw=source.read_bytes();s=json.loads(raw);d=json.loads(fixture.read_text());
 if H(raw)!=c['source_record_sha256'] or H((P/'source_extract.txt').read_bytes())!=c['source_extract_sha256']:return {'status':'REJECT','reason':'SOURCE_IDENTITY'}
 if d.get('source_sha256')!=c['source_record_sha256']:return {'status':'REJECT','reason':'SOURCE_REFERENCE'}
 for k in ['material','phase','reference_temperature_K','reference_pressure']:
  expected={'material':s['material'],'phase':s['phase'],'reference_temperature_K':s['temperature_K'],'reference_pressure':s['pressure']}[k]
  if d.get(k)!=expected:return {'status':'REJECT','reason':'MATERIAL_OR_CONDITIONS','field':k}
 if d.get('cp_unit')!=s['property_unit'] or d.get('molar_mass_unit')!='g/mol' or d.get('heat_unit')!='kJ':return {'status':'REJECT','reason':'UNIT'}
 try:mass=F(d['mass_g']);mw=F(s['molecular_weight_value']);cp=F(s['property_value']);heat=F(d['heat_input_kJ'])*1000
 except (ValueError,ZeroDivisionError,TypeError,KeyError):return {'status':'REJECT','reason':'INVALID_INPUT'}
 if mass<=0 or mw<=0 or cp<=0 or heat<0:return {'status':'REJECT','reason':'DOMAIN'}
 quantity={'amount_mol':str(mass/mw)}
 if handoff is not None and handoff!=quantity:return {'status':'REJECT','reason':'HANDOFF_MISMATCH'}
 n=F((quantity if handoff is None else handoff)['amount_mol']);delta=heat/(n*cp)
 stages=[s,{'status':'PASS','material':s['material'],'phase':s['phase'],'reference_temperature_K':s['temperature_K'],'reference_pressure':s['pressure'],'units':'PASS'}, {'mass_g':str(mass),'heat_input_J':str(heat),'cp_J_per_mol_K':str(cp),'molar_mass_g_per_mol':str(mw)},quantity,{'temperature_change_K':str(delta),'formula':'Q_J / (n_mol * Cp_J_per_mol_K)'},{'status':'PASS','assumption':'Cp held constant for small temperature change; no losses or phase change','source_scope':'298 K row; pressure and uncertainty not numerically specified in selected table'}];out.mkdir();hashes={}
 for name,value in zip(N,stages):
  b=encode(value);(out/name).write_bytes(b);hashes[name]=H(b)
 (out/'07_commitment.json').write_bytes(encode({'algorithm':'sha256','artifacts':hashes}));return {'status':'PASS','temperature_change_K':str(delta)}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',type=pathlib.Path,default=P/'source_record.json');a.add_argument('--fixture',type=pathlib.Path,default=P/'fixture.json');a.add_argument('--handoff',type=pathlib.Path);a.add_argument('--out',type=pathlib.Path,required=True);z=a.parse_args();r=run(z.source,z.fixture,z.out,json.loads(z.handoff.read_text()) if z.handoff else None);print(json.dumps(r,sort_keys=True));sys.exit(0 if r['status']=='PASS' else 2)
