import argparse,hashlib,json,pathlib
NAMES=['01_input.json','02_budget.json','03_plan.json','04_allocations.json','05_unmet.json','06_balance.json','07_decision.json']
def canon(v): return (json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def generate(x):
 if set(x)!={'supply','reserve','sites'} or any(type(x[k]) is not int or x[k]<0 for k in ('supply','reserve')) or x['reserve']>x['supply'] or type(x['sites']) is not list: raise ValueError('input')
 seen=set(); ranks=set()
 for s in x['sites']:
  if type(s) is not dict or set(s)!={'id','priority','demand'} or type(s['id']) is not str or not s['id'] or type(s['priority']) is not int or s['priority']<1 or type(s['demand']) is not int or s['demand']<0 or s['id'] in seen or s['priority'] in ranks: raise ValueError('site')
  seen.add(s['id']);ranks.add(s['priority'])
 plan=sorted(x['sites'],key=lambda z:(z['priority'],z['id'])); budget=x['supply']-x['reserve'];left=budget;alloc=[]
 for s in plan:
  n=min(s['demand'],left);left-=n;alloc.append({'id':s['id'],'liters':n})
 unmet=[{'id':s['id'],'liters':s['demand']-a['liters']} for s,a in zip(plan,alloc)]
 balance={'allocated':sum(a['liters'] for a in alloc),'remaining':left,'reserve':x['reserve'],'supply':x['supply'],'unmet':sum(a['liters'] for a in unmet)}
 decision={'status':'SHORTFALL' if balance['unmet'] else 'SATISFIED','unmet_liters':balance['unmet']}
 return [x,{'usable_liters':budget},plan,alloc,unmet,balance,decision]
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--out',required=True);a=p.parse_args();x=json.loads(pathlib.Path(a.input).read_text());items=generate(x);out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=False)
 for name,obj in zip(NAMES,items): (out/name).write_bytes(canon(obj))
 print(json.dumps({'status':'PASS','artifacts':{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in NAMES}},sort_keys=True))
if __name__=='__main__':main()
