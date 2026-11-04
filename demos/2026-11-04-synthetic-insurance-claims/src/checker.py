import json,sys,pathlib,hashlib,re

def error(s,n):print(json.dumps({'status':s},sort_keys=True));sys.exit(n)
def unique(p):
 if len(p)!=len(dict(p)):raise ValueError('duplicate key')
 return dict(p)
def reject(_):raise ValueError('numeric format')
def keys(o,ks):
 if not isinstance(o,dict) or sorted(o)!=sorted(ks):raise ValueError('shape')
def word(v):
 if type(v) is not str or re.fullmatch(r'[\x21-\x7e]+',v) is None:raise ValueError('string')
def integer(v):
 if type(v) is not int or v<0 or v>1000000000:raise ValueError('integer')
def parse(path):
 d=json.loads(pathlib.Path(path).read_bytes().decode('utf8'),object_pairs_hook=unique,parse_float=reject,parse_constant=reject)
 keys(d,['policy','claimant','claims']);p=d['policy'];keys(p,['id','covered','excluded','deductible','limit','authority']);word(p['id']);keys(d['claimant'],['id']);word(d['claimant']['id'])
 for k in ['deductible','limit','authority']:integer(p[k])
 for k in ['covered','excluded']:
  a=p[k]
  if type(a)!=list:raise ValueError('list')
  for x in a:word(x)
  if len(set(a))!=len(a):raise ValueError('duplicates')
  p[k]=sorted(a)
 if set(p['excluded']).intersection(p['covered']):raise ValueError('overlap')
 if type(d['claims'])!=list:raise ValueError('claims')
 ids=[]
 for c in d['claims']:
  keys(c,['id','policy_id','claimant_id','cause','amount','evidence']);integer(c['amount'])
  for k in ['id','policy_id','claimant_id','cause']:word(c[k])
  ids.append(c['id'])
  if type(c['evidence'])!=list:raise ValueError('evidence')
  for e in c['evidence']:
   keys(e,['claim_id','policy_id','cause'])
   for k in e:word(e[k])
  c['evidence']=sorted(c['evidence'],key=lambda x:(x['claim_id'],x['policy_id'],x['cause']))
 if len(ids)!=len(set(ids)):raise ValueError('duplicates')
 d['claims']=sorted(d['claims'],key=lambda x:x['id']);return d
def encode(v):return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode('utf-8')
def independently_recompute(data):
 p=data['policy'];coverage=[];evidence=[];calculations=[];decisions=[];dispositions=[]
 for claim in data['claims']:
  cid=claim['id'];cause=claim['cause'];records=claim['evidence']
  classification= 'EXCLUDED' if cause in p['excluded'] else ('COVERED' if cause in p['covered'] else 'NOT_COVERED')
  coverage.append(dict(id=cid,coverage=classification))
  if len(records)==0:status='EVIDENCE_MISSING'
  elif len(records)>1:status='EVIDENCE_DUPLICATE'
  elif (claim['policy_id'],claim['claimant_id'],records[0]['claim_id'],records[0]['policy_id'])!=(p['id'],data['claimant']['id'],cid,p['id']):status='BINDING_MISMATCH'
  elif records[0]['cause']!=cause:status='EVIDENCE_CONFLICT'
  else:status='OK'
  evidence.append(dict(id=cid,status=status))
  value=None
  if status=='OK' and classification=='COVERED':value=min(p['limit'],max(0,claim['amount']-p['deductible']))
  calculations.append(dict(id=cid,provisional_amount=value,within_authority=None if value is None else value<=p['authority']))
  if status!='OK':action='HOLD';reason=status
  elif classification=='EXCLUDED':action='DENY';reason='EXCLUDED_CAUSE'
  elif classification=='NOT_COVERED':action='DENY';reason='NOT_COVERED'
  elif value==0:action='HOLD';reason='ZERO_AMOUNT'
  elif value>p['authority']:action='HOLD';reason='AUTHORITY_EXCEEDED'
  else:action='ROUTE_PAYMENT';reason='COVERED_WITHIN_AUTHORITY'
  decisions.append(dict(id=cid,decision=action,reasons=[reason]));dispositions.append(dict(id=cid,disposition=action,amount=value if action=='ROUTE_PAYMENT' else 0))
 return [data,coverage,evidence,calculations,decisions,dispositions]
N=['01_inputs.json','02_coverage.json','03_evidence.json','04_calculation.json','05_decisions.json','06_disposition.json','07_commitment.json']
def main():
 if len(sys.argv)!=3:error('INVALID_INPUT',2)
 try:data=parse(sys.argv[1])
 except (OSError,UnicodeError,ValueError,TypeError,RecursionError):error('INVALID_INPUT',2)
 expected=[encode(x) for x in independently_recompute(data)]
 expected.append(encode({N[i]:hashlib.sha256(b).hexdigest() for i,b in enumerate(expected)}))
 try:
  actual=[(pathlib.Path(sys.argv[2])/n).read_bytes() for n in N]
 except OSError:error('CHECK_FAILED',1)
 if actual!=expected:error('CHECK_FAILED',1)
 print(json.dumps({'status':'OK'},sort_keys=True))
if __name__=='__main__':main()
