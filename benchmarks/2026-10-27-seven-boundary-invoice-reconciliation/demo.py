import argparse, hashlib, json, pathlib

def encode(v):
    return (json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)+'\n').encode()

def build(data):
    rows=data['invoices']
    lines=[{'row':i,'amount_cents':r['quantity']*r['unit_cents']} for i,r in enumerate(rows)]
    limits=[{'row':i,'within_limit':lines[i]['amount_cents']<=r['limit_cents']} for i,r in enumerate(rows)]
    seen=set(); duplicates=[]
    for i,r in enumerate(rows):
        key=(r['vendor'],r['invoice']); duplicates.append({'row':i,'duplicate':key in seen}); seen.add(key)
    decisions=[{'row':i,'status':'HOLD_DUPLICATE' if duplicates[i]['duplicate'] else 'PAY' if limits[i]['within_limit'] else 'HOLD_LIMIT','amount_cents':lines[i]['amount_cents']} for i in range(len(rows))]
    ledger={'payable_cents':sum(d['amount_cents'] for d in decisions if d['status']=='PAY'),'held_cents':sum(d['amount_cents'] for d in decisions if d['status']!='PAY'),'total_cents':sum(d['amount_cents'] for d in decisions)}
    vals=[data,lines,limits,duplicates,decisions,ledger]
    names=['01_input.json','02_amounts.json','03_limits.json','04_duplicates.json','05_dispositions.json','06_ledger.json']
    outputs={name:encode(v) for name,v in zip(names,vals)}
    outputs['07_commitment.json']=encode({'ledger':ledger,'sha256':{k:hashlib.sha256(v).hexdigest() for k,v in outputs.items()}})
    return outputs

def verify(outputs):
    commitment=json.loads(outputs['07_commitment.json']); expected=commitment['sha256']
    return set(expected)==set(outputs)-{'07_commitment.json'} and all(hashlib.sha256(outputs[k]).hexdigest()==v for k,v in expected.items())

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--out',required=True); a=p.parse_args()
    out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=False)
    artifacts=build(json.loads(pathlib.Path(a.input).read_text()))
    for name,value in artifacts.items(): (out/name).write_bytes(value)
    print(json.dumps({'status':'PASS','artifact_count':len(artifacts),'integrity':verify(artifacts)},sort_keys=True))
if __name__=='__main__': main()
