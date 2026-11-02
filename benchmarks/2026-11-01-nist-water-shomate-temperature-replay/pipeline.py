import json,hashlib,pathlib,argparse,sys
from fractions import Fraction as F
P=pathlib.Path(__file__).resolve().parent; E=lambda x:(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode(); H=lambda b:hashlib.sha256(b).hexdigest();S=lambda x:str(F(x));N=['01_source.json','02_validation.json','03_fixture.json','04_cp.json','05_integral.json','06_comparison.json']
def run(sp,fp,out,handoff=None):
 c=json.loads((P/'CONTRACT.json').read_text());raw=sp.read_bytes();s=json.loads(raw);f=json.loads(fp.read_text());
 if H(raw)!=c['source_record_sha256'] or H((P/'source_extract.txt').read_bytes())!=c['extract_sha256']:return {'status':'REJECT','reason':'SOURCE_IDENTITY'}
 if f.get('source_sha256')!=c['source_record_sha256']:return {'status':'REJECT','reason':'SOURCE_REFERENCE'}
 if f.get('temperature_unit')!='K' or f.get('energy_unit')!='J':return {'status':'REJECT','reason':'UNIT'}
 if f.get('material')!=s['material'] or f.get('phase')!=s['phase'] or f.get('pressure')!=s['pressure']:return {'status':'REJECT','reason':'CONDITIONS'}
 try:lo=F(f['temperature_start']);hi=F(f['temperature_end']);amount=F(f['amount_mol'])
 except (KeyError,ValueError,TypeError,ZeroDivisionError):return {'status':'REJECT','reason':'SCHEMA'}
 if lo<F(298) or hi>F(500) or hi<=lo or amount<=0:return {'status':'REJECT','reason':'RANGE'}
 a,b,c0,d,e=[F(s['coefficients'][k]) for k in 'ABCDE'];t0=lo/1000;t1=hi/1000;cp=lambda t:a+b*t+c0*t*t+d*t*t*t+e/(t*t); stages=[s,{'status':'PASS','material':'water','phase':'liquid','source_range_K':['298','500'],'unit':'K','energy_unit':'J','pressure':s['pressure']},{'amount_mol':S(amount),'start_K':S(lo),'end_K':S(hi),'source_sha256':f['source_sha256']},{'cp_start_J_per_mol_K':S(cp(t0)),'cp_end_J_per_mol_K':S(cp(t1))}];
 if handoff is not None and handoff!=stages[-1]:return {'status':'REJECT','reason':'HANDOFF'}
 q=amount*1000*(a*(t1-t0)+b*(t1*t1-t0*t0)/2+c0*(t1**3-t0**3)/3+d*(t1**4-t0**4)/4+e*(1/t0-1/t1));fixed=amount*F('75.38')*(hi-lo);stages += [{'heat_J':S(q),'method':'analytic exact rational integral of Shomate Cp'},{'constant_heat_J':S(fixed),'difference_integrated_minus_constant_J':S(q-fixed),'constant_cp_J_per_mol_K':'3769/50','limitations':'Rounded 298 K table value and constant Cp approximation; no experiment; pressure and uncertainty not numerically stated.'}];out.mkdir();hashes={}
 for name,obj in zip(N,stages):b=E(obj);(out/name).write_bytes(b);hashes[name]=H(b)
 (out/'07_commitment.json').write_bytes(E({'algorithm':'sha256','artifacts':hashes}));return {'status':'PASS','heat_J':S(q),'constant_J':S(fixed),'difference_J':S(q-fixed)}
if __name__=='__main__':
 x=argparse.ArgumentParser();x.add_argument('--source',type=pathlib.Path,default=P/'source_record.json');x.add_argument('--fixture',type=pathlib.Path,default=P/'fixture.json');x.add_argument('--handoff',type=pathlib.Path);x.add_argument('--out',type=pathlib.Path,required=True);z=x.parse_args();v=run(z.source,z.fixture,z.out,json.loads(z.handoff.read_text()) if z.handoff else None);print(json.dumps(v,sort_keys=True));sys.exit(0 if v['status']=='PASS' else 2)
