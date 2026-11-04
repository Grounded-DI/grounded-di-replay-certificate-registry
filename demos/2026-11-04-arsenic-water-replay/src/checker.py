import json,sys,pathlib,hashlib,re
from decimal import Decimal,InvalidOperation
N=['01_source.json','02_inputs.json','03_eligibility.json','04_comparison.json','05_report.json','06_commitment.json'];S={'id':'EPA_ARSENIC_MCL','threshold':'10','unit':'ug/L','url':'https://www.epa.gov/ground-water-and-drinking-water/national-primary-drinking-water-regulations'}
def end(s,c):print(json.dumps({'status':s}));sys.exit(c)
def pairs(x):
 if len(x)!=len(dict(x)):raise ValueError()
 return dict(x)
def valid_num(n):
 if type(n)!=str or re.fullmatch(r'(0|[1-9][0-9]*)(\.[0-9]{1,6})?',n) is None or Decimal(n)>1000000:raise ValueError()
def get_input(path):
 try:d=json.loads(pathlib.Path(path).read_bytes().decode('utf8'),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError()))
 except (OSError,UnicodeError,ValueError,RecursionError):end('INVALID_INPUT',2)
 if type(d)!=dict:end('INVALID_INPUT',2)
 if d.get('source')!=S:end('INVALID_SOURCE',2)
 try:
  if sorted(d)!=['samples','source'] or type(d['samples'])!=list:raise ValueError()
  seen=set()
  for s in d['samples']:
   if type(s)!=dict or set(s)!={'id','context','status','result','unit','reporting_limit'}:raise ValueError()
   ident=s['id']
   if type(ident)!=str or not re.fullmatch(r'[A-Za-z0-9]+',ident) or ident in seen:raise ValueError()
   seen.add(ident)
   if type(s['context'])!=str or type(s['unit'])!=str or s['status'] not in ['quantified','below_limit']:raise ValueError()
   valid_num(s['reporting_limit'])
   if s['status']=='quantified':valid_num(s['result'])
   elif s['result'] is not None:raise ValueError()
 except (ValueError,TypeError,InvalidOperation):end('INVALID_INPUT',2)
 d['samples']=sorted(d['samples'],key=lambda x:x['id']);return d
def dump(v):return (json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':'))+'\n').encode()
def recompute(d):
 e=[];c=[]
 for s in d['samples']:
  if s['context']!='entry_point':reason='CONTEXT_OUT_OF_SCOPE'
  elif s['unit'] not in ('ug/L','mg/L'):reason='UNIT_UNSUPPORTED'
  elif s['status']=='below_limit':reason='BELOW_REPORTING_LIMIT'
  elif Decimal(s['result'])<Decimal(s['reporting_limit']):reason='INCONSISTENT_RESULT'
  else:reason='NUMERIC_COMPARISON'
  value=None if reason!='NUMERIC_COMPARISON' else Decimal(s['result'])*(Decimal(1000) if s['unit']=='mg/L' else Decimal(1))
  if value is None:formatted=None;comparison='HOLD'
  else:
   formatted=format(value,'f');formatted=formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted
   comparison='BELOW' if value<Decimal(10) else 'EQUAL' if value==Decimal(10) else 'ABOVE'
  e.append(dict(id=s['id'],eligible=value is not None,reason=reason,ug_per_l=formatted));c.append(dict(id=s['id'],comparison=comparison,reason=reason))
 notes=[]
 for record,decision in zip(e,c):
  ident=record['id'];reason=record['reason']
  if reason=='NUMERIC_COMPARISON':
   relation={'BELOW':'below','ABOVE':'above','EQUAL':'equal to'}[decision['comparison']]
   notes.append('Sample '+ident+': '+record['ug_per_l']+' µg/L is '+relation+' the 10 µg/L reference.')
  else:
   message={'CONTEXT_OUT_OF_SCOPE':'the sample context is outside this demonstration','UNIT_UNSUPPORTED':'the unit is missing or unsupported','BELOW_REPORTING_LIMIT':'the result is below the reporting limit','INCONSISTENT_RESULT':'the quantified result is below the reporting limit'}[reason]
   notes.append('Sample '+ident+': comparison held because '+message+'.')
 return [d['source'],d['samples'],e,c,{'notice':'Numerical comparison only; not compliance, safety, or health-risk determination.','results':c,'explanations':notes}]
def main():
 if len(sys.argv)!=3:end('INVALID_INPUT',2)
 data=get_input(sys.argv[1]);blobs=[dump(x) for x in recompute(data)];blobs.append(dump({N[i]:hashlib.sha256(b).hexdigest() for i,b in enumerate(blobs)}))
 try:got=[(pathlib.Path(sys.argv[2])/name).read_bytes() for name in N]
 except OSError:end('CHECK_FAILED',1)
 if blobs!=got:end('CHECK_FAILED',1)
 end('OK',0)
if __name__=='__main__':main()
