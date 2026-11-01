import sys,json,hashlib
from pathlib import Path
from datetime import date,timedelta

def encode(x): return (json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)+'\n').encode()
def generate(inp,out):
 p=Path(out);p.mkdir();cases=sorted(inp['cases'],key=lambda c:c['id'])
 def save(name,data):
  data=encode(data);(p/name).write_bytes(data);return hashlib.sha256(data).hexdigest()
 hashes={};hashes['01_input.json']=save('01_input.json',cases)
 hashes['02_rule.json']=save('02_rule.json',{'calendar_days':10,'weekend':'next_monday','holidays':[]})
 gates=[{'id':c['id'],'status':'READY' if len(c['service_dates'])==1 else 'HOLD'} for c in cases];hashes['03_gates.json']=save('03_gates.json',gates)
 raw=[]
 for c,g in zip(cases,gates):
  if g['status']=='READY':
   try: raw.append({'id':c['id'],'raw':(date.fromisoformat(c['service_dates'][0])+timedelta(days=10)).isoformat()})
   except ValueError:raw.append({'id':c['id'],'raw':None})
  else:raw.append({'id':c['id'],'raw':None})
 hashes['04_raw.json']=save('04_raw.json',raw)
 adj=[]
 for x in raw:
  d=date.fromisoformat(x['raw']) if x['raw'] else None
  if d and d.weekday()>=5:d+=timedelta(days=7-d.weekday())
  adj.append({'id':x['id'],'deadline':d.isoformat() if d else None})
 hashes['05_adjusted.json']=save('05_adjusted.json',adj)
 final=[{'id':g['id'],'status':'READY' if a['deadline'] else 'HOLD','deadline':a['deadline']} for g,a in zip(gates,adj)];hashes['06_decisions.json']=save('06_decisions.json',final)
 save('07_commitment.json',hashes)
if __name__=='__main__':generate(json.loads(Path(sys.argv[1]).read_text()),sys.argv[2])
