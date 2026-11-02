import argparse,pathlib,json,hashlib,sys
from fractions import Fraction as F
P=pathlib.Path(__file__).resolve().parent
U={'material_amount':'mol','energy_per_mole':'kJ/mol','capture_fraction':'1','water_mass':'kg','heat_capacity':'J/(kg*K)'}
N=['01_inputs.json','02_moles.json','03_chemistry_energy.json','04_transfer.json','05_temperature.json','06_checks.json']
def encode(x):return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def h(b):return hashlib.sha256(b).hexdigest()
def run(d,out,handoff=None):
 if not isinstance(d,dict) or set(d)!=set(U):return {'status':'REJECT','reason':'SCHEMA'}
 try:
  for k,unit in U.items():
   if not isinstance(d[k],dict) or set(d[k])!={'value','unit'} or d[k]['unit']!=unit:return {'status':'REJECT','reason':'UNIT_OR_SCHEMA','field':k}
  vals={k:F(d[k]['value']) for k in U}
 except (ValueError,ZeroDivisionError,TypeError,KeyError):return {'status':'REJECT','reason':'INVALID_NUMBER'}
 n,e,cap,m,cp=[vals[k] for k in U]
 if n<0 or e<0:return {'status':'REJECT','reason':'NEGATIVE_CHEMISTRY'}
 if not 0<=cap<=1:return {'status':'REJECT','reason':'CAPTURE_RANGE'}
 if m<=0 or cp<=0:return {'status':'REJECT','reason':'NONPOSITIVE_DENOMINATOR'}
 norm={k:{'value':str(vals[k]),'unit':U[k]} for k in U}; q=n*e*1000;chem={'energy_release':{'value':str(q),'unit':'J'}}
 if handoff is not None and handoff!=chem:return {'status':'REJECT','reason':'CHEMISTRY_HANDOFF_MISMATCH'}
 received=chem if handoff is None else handoff; q2=F(received['energy_release']['value'])*cap;t=q2/(m*cp)
 stages=[norm,{'amount_mol':str(n)},chem,{'transferred_energy':{'value':str(q2),'unit':'J'}},{'temperature_change':{'value':str(t),'unit':'K'}},{'status':'PASS','checks':{'capture_range':True,'positive_heat_capacity':True,'positive_mass':True,'units_valid':True}}];out.mkdir(); hashes={}
 for name,value in zip(N,stages):
  b=encode(value);(out/name).write_bytes(b);hashes[name]=h(b)
 (out/'07_commitment.json').write_bytes(encode({'algorithm':'sha256','artifacts':hashes}));return {'status':'PASS','temperature_change_K':str(t)}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--fixture',type=pathlib.Path,default=P/'fixture.json');a.add_argument('--out',type=pathlib.Path,required=True);a.add_argument('--handoff',type=pathlib.Path);z=a.parse_args();r=run(json.loads(z.fixture.read_text()),z.out,json.loads(z.handoff.read_text()) if z.handoff else None);print(json.dumps(r,sort_keys=True));sys.exit(0 if r['status']=='PASS' else 2)
