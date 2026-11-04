import sys,json,hashlib,pathlib,re

def fail(code,exit): print(json.dumps({'status':code},sort_keys=True));sys.exit(exit)
def pairs(p):
 d={}
 for k,v in p:
  if k in d: raise ValueError('duplicate key')
  d[k]=v
 return d
def load(path):
 return json.loads(pathlib.Path(path).read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError()),parse_float=lambda x: (_ for _ in ()).throw(ValueError()))
def obj(x,keys):
 if type(x)!=dict or set(x)!=set(keys): raise ValueError('keys')
def name(x):
 if type(x)!=str or not re.fullmatch(r'[\x21-\x7e]+',x): raise ValueError('name')
def num(x):
 if type(x)!=int or not 0<=x<=1000000000: raise ValueError('amount')
def normalize(d):
 obj(d,['policy','claimant','claims']);p=d['policy'];obj(p,['id','covered','excluded','deductible','limit','authority']);name(p['id']);obj(d['claimant'],['id']);name(d['claimant']['id'])
 for k in ('deductible','limit','authority'):num(p[k])
 for k in ('covered','excluded'):
  if type(p[k])!=list or len(set(p[k]))!=len(p[k]):raise ValueError('list')
  for s in p[k]:name(s)
  p[k].sort()
 if set(p['covered'])&set(p['excluded']):raise ValueError('overlap')
 if type(d['claims'])!=list:raise ValueError('claims')
 seen=set()
 for c in d['claims']:
  obj(c,['id','policy_id','claimant_id','cause','amount','evidence'])
  for k in ('id','policy_id','claimant_id','cause'):name(c[k])
  if c['id'] in seen:raise ValueError('duplicate')
  seen.add(c['id']);num(c['amount'])
  if type(c['evidence'])!=list:raise ValueError('evidence')
  for e in c['evidence']:
   obj(e,['claim_id','policy_id','cause'])
   for x in e.values():name(x)
  c['evidence'].sort(key=lambda e:(e['claim_id'],e['policy_id'],e['cause']))
 d['claims'].sort(key=lambda c:c['id']);return d
def encode(o):return (json.dumps(o,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def make(d):
 p=d['policy'];out=[d];cov=[];evs=[];cal=[];dec=[];disp=[]
 for c in d['claims']:
  cause=c['cause'];coverage='EXCLUDED' if cause in p['excluded'] else 'COVERED' if cause in p['covered'] else 'NOT_COVERED';cov.append({'id':c['id'],'coverage':coverage})
  es=c['evidence'];status='OK'
  if not es:status='EVIDENCE_MISSING'
  elif len(es)>1:status='EVIDENCE_DUPLICATE'
  elif c['policy_id']!=p['id'] or c['claimant_id']!=d['claimant']['id'] or es[0]['policy_id']!=p['id'] or es[0]['claim_id']!=c['id']:status='BINDING_MISMATCH'
  elif es[0]['cause']!=cause:status='EVIDENCE_CONFLICT'
  evs.append({'id':c['id'],'status':status})
  amount=min(max(c['amount']-p['deductible'],0),p['limit']) if status=='OK' and coverage=='COVERED' else None
  cal.append({'id':c['id'],'provisional_amount':amount,'within_authority':amount<=p['authority'] if amount is not None else None})
  if status!='OK':decision,reason='HOLD',status
  elif coverage=='EXCLUDED':decision,reason='DENY','EXCLUDED_CAUSE'
  elif coverage=='NOT_COVERED':decision,reason='DENY','NOT_COVERED'
  elif amount==0:decision,reason='HOLD','ZERO_AMOUNT'
  elif amount>p['authority']:decision,reason='HOLD','AUTHORITY_EXCEEDED'
  else:decision,reason='ROUTE_PAYMENT','COVERED_WITHIN_AUTHORITY'
  dec.append({'id':c['id'],'decision':decision,'reasons':[reason]});disp.append({'id':c['id'],'disposition':decision,'amount':amount if decision=='ROUTE_PAYMENT' else 0})
 out += [cov,evs,cal,dec,disp];return out
N=['01_inputs.json','02_coverage.json','03_evidence.json','04_calculation.json','05_decisions.json','06_disposition.json','07_commitment.json']
def main():
 if len(sys.argv)!=3:fail('INVALID_INPUT',2)
 try:d=normalize(load(sys.argv[1]))
 except (OSError,ValueError,TypeError,UnicodeError,RecursionError):fail('INVALID_INPUT',2)
 dest=pathlib.Path(sys.argv[2])
 if dest.exists():fail('OUTPUT_EXISTS',2)
 try:
  dest.mkdir(); blobs=[encode(x) for x in make(d)];blobs.append(encode({N[i]:hashlib.sha256(b).hexdigest() for i,b in enumerate(blobs)}))
  for n,b in zip(N,blobs):(dest/n).write_bytes(b)
 except OSError:fail('IO_ERROR',3)
 print(json.dumps({'status':'OK'},sort_keys=True))
if __name__=='__main__':main()
