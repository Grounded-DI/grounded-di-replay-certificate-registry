import argparse,hashlib,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parent
N=['01_request.json','02_artifact.json','03_tests.json','04_approval.json','05_policy.json','06_decision.json']
def encode(x): return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def digest(x): return hashlib.sha256(x).hexdigest()
def evaluate(req,policy,evidence,artifact):
 req=req if isinstance(req,dict) else {}; pol=policy if isinstance(policy,dict) else {}; ev=evidence if isinstance(evidence,dict) else {}
 normalized={k:req.get(k) for k in ('artifact_sha256','candidate_id','destination','policy_sha256')}; valid=all(isinstance(normalized[k],str) and normalized[k] for k in normalized); a=digest(artifact); ph=digest(encode(pol)); prov=ev.get('provenance') or {}; approval=ev.get('approval') or {}; tests=ev.get('tests') or []; tests=tests if isinstance(tests,list) else []
 ac={'artifact_identity':bool(valid and a==req.get('artifact_sha256')),'provenance':bool(valid and isinstance(prov,dict) and prov.get('artifact_sha256')==a and prov.get('candidate_id')==req.get('candidate_id') and prov.get('source')=='fixture-source-v1')}
 tc={n:sum(isinstance(t,dict) and t.get('name')==n and t.get('status')=='PASS' for t in tests)==1 and sum(isinstance(t,dict) and t.get('name')==n for t in tests)==1 for n in ('format','unit')}
 binding=bool(valid and isinstance(approval,dict) and approval.get('role')=='synthetic-reviewer' and all(approval.get(k)==req.get(k) for k in ('candidate_id','artifact_sha256','destination','policy_sha256')))
 pc={'destination':bool(valid and req.get('destination')==pol.get('destination')=='synthetic/releases/v1'),'policy_binding':bool(valid and req.get('policy_sha256')==ph)}
 checks={**ac,**tc,'approval_binding':binding,**pc};reasons=sorted(k for k,v in checks.items() if not v);return [normalized,{'artifact_sha256':a,'checks':ac,'stage':'artifact'},{'checks':tc,'stage':'tests'},{'checks':{'approval_binding':binding},'stage':'approval'},{'checks':pc,'stage':'policy'},{'decision':'ELIGIBLE' if not reasons else 'HOLD','reasons':reasons}]
def build(src,out):
 req=json.loads((src/'request.json').read_text());policy=json.loads((src/'policy.json').read_text());ev=json.loads((src/'evidence.json').read_text()); artifact=(src/'artifact.bin').read_bytes(); stages=evaluate(req,policy,ev,artifact);out.mkdir(); hashes={}
 for name,stage in zip(N,stages):
  b=encode(stage);(out/name).write_bytes(b);hashes[name]=digest(b)
 (out/'07_commitment.json').write_bytes(encode({'algorithm':'sha256','artifacts':hashes}));return stages[-1]
def promote(src,out,dest):
 # Recalculate and compare all stage bytes before touching the destination.
 expected=evaluate(json.loads((src/'request.json').read_text()),json.loads((src/'policy.json').read_text()),json.loads((src/'evidence.json').read_text()),(src/'artifact.bin').read_bytes());
 try:
  contents=[(out/n).read_bytes() for n in N];commit=(out/'07_commitment.json').read_bytes(); valid=all(a==encode(b) for a,b in zip(contents,expected)) and commit==encode({'algorithm':'sha256','artifacts':{n:digest(b) for n,b in zip(N,contents)}}) and expected[-1]['decision']=='ELIGIBLE'
 except (OSError,ValueError): valid=False
 if not valid:return 'REJECT'
 dest.mkdir(parents=True,exist_ok=True);(dest/'promoted.bin').write_bytes((src/'artifact.bin').read_bytes());return 'WROTE'
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--src',type=pathlib.Path,default=P);a.add_argument('--out',type=pathlib.Path,required=True);a.add_argument('--promote',type=pathlib.Path);v=a.parse_args(); result=build(v.src,v.out); print(json.dumps(result,sort_keys=True));
 if v.promote: print('promotion='+promote(v.src,v.out,v.promote))
