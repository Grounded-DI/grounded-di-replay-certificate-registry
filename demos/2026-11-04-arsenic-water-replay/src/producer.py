import sys,json,pathlib,hashlib,re,decimal
from decimal import Decimal
S={'id':'EPA_ARSENIC_MCL','threshold':'10','unit':'ug/L','url':'https://www.epa.gov/ground-water-and-drinking-water/national-primary-drinking-water-regulations'}
N=['01_source.json','02_inputs.json','03_eligibility.json','04_comparison.json','05_report.json','06_commitment.json'];NOTICE='Numerical comparison only; not compliance, safety, or health-risk determination.'
def fail(s,c):print(json.dumps({'status':s}));sys.exit(c)
def unique(p):
 d={}
 for k,v in p:
  if k in d:raise ValueError()
  d[k]=v
 return d
def num(x):
 if type(x)!=str or not re.fullmatch(r'(0|[1-9][0-9]*)(\.[0-9]{1,6})?',x) or Decimal(x)>1000000:raise ValueError()
def load(p):
 try:d=json.loads(pathlib.Path(p).read_text(encoding='utf8'),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in ()).throw(ValueError()))
 except (ValueError,OSError,UnicodeError,RecursionError):fail('INVALID_INPUT',2)
 if type(d)!=dict:fail('INVALID_INPUT',2)
 if d.get('source')!=S:fail('INVALID_SOURCE',2)
 try:
  if set(d)!={'source','samples'} or type(d['samples'])!=list:raise ValueError()
  ids=[]
  for s in d['samples']:
   if type(s)!=dict or set(s)!={'id','context','status','result','unit','reporting_limit'}:raise ValueError()
   if type(s['id'])!=str or not re.fullmatch(r'[A-Za-z0-9]+',s['id']):raise ValueError()
   ids.append(s['id'])
   if type(s['context'])!=str or type(s['unit'])!=str or s['status'] not in ('quantified','below_limit'):raise ValueError()
   num(s['reporting_limit'])
   if s['status']=='quantified':num(s['result'])
   elif s['result'] is not None:raise ValueError()
  if len(ids)!=len(set(ids)):raise ValueError()
 except (ValueError,TypeError,decimal.InvalidOperation):fail('INVALID_INPUT',2)
 d['samples'].sort(key=lambda x:x['id']);return d
def encode(x):return (json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def records(d):
 es=[];cs=[]
 for x in d['samples']:
  why='NUMERIC_COMPARISON';v=None
  if x['context']!='entry_point':why='CONTEXT_OUT_OF_SCOPE'
  elif x['unit'] not in ('ug/L','mg/L'):why='UNIT_UNSUPPORTED'
  elif x['status']=='below_limit':why='BELOW_REPORTING_LIMIT'
  elif Decimal(x['result'])<Decimal(x['reporting_limit']):why='INCONSISTENT_RESULT'
  else:v=Decimal(x['result'])*(1000 if x['unit']=='mg/L' else 1)
  vs=(format(v,'f').rstrip('0').rstrip('.') if '.' in format(v,'f') else format(v,'f')) if v is not None else None
  es.append({'id':x['id'],'eligible':v is not None,'reason':why,'ug_per_l':vs})
  c='HOLD' if v is None else ('ABOVE' if v>10 else 'BELOW' if v<10 else 'EQUAL');cs.append({'id':x['id'],'comparison':c,'reason':why})
 sentences=[]
 for e,c in zip(es,cs):
  label=e['id'];why=e['reason'];value=e['ug_per_l']
  if why=='NUMERIC_COMPARISON':
   rel={'ABOVE':'above','BELOW':'below','EQUAL':'equal to'}[c['comparison']];sentence=f'Sample {label}: {value} µg/L is {rel} the 10 µg/L reference.'
  else:
   detail={'CONTEXT_OUT_OF_SCOPE':'the sample context is outside this demonstration','UNIT_UNSUPPORTED':'the unit is missing or unsupported','BELOW_REPORTING_LIMIT':'the result is below the reporting limit','INCONSISTENT_RESULT':'the quantified result is below the reporting limit'}[why];sentence=f'Sample {label}: comparison held because {detail}.'
  sentences.append(sentence)
 return [d['source'],d['samples'],es,cs,{'notice':NOTICE,'results':cs,'explanations':sentences}]
def main():
 if len(sys.argv)!=3:fail('INVALID_INPUT',2)
 d=load(sys.argv[1]);out=pathlib.Path(sys.argv[2])
 if out.exists():fail('OUTPUT_EXISTS',2)
 try:
  out.mkdir();blobs=[encode(x) for x in records(d)];blobs.append(encode({N[i]:hashlib.sha256(x).hexdigest() for i,x in enumerate(blobs)}))
  for n,b in zip(N,blobs):(out/n).write_bytes(b)
 except OSError:fail('IO_ERROR',3)
 fail('OK',0)
if __name__=='__main__':main()
