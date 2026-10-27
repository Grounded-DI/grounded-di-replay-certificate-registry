import argparse, hashlib, json, pathlib

def encode(obj):
    return (json.dumps(obj,sort_keys=True,separators=(',', ':'),ensure_ascii=True,allow_nan=False)+'\n').encode('utf-8')

def build(data):
    readings=data['readings']
    if not readings or readings[0]['minute'] != 0 or any(b['minute'] <= a['minute'] for a,b in zip(readings,readings[1:])):
        raise ValueError('timestamps must start at zero and increase')
    calibrated=[{'minute':x['minute'],'temp_tenths':x['temp_tenths']+data['calibration_tenths']} for x in readings]
    temps=[{'minute':x['minute'],'temp_tenths':x['temp_tenths'],'in_range':20<=x['temp_tenths']<=80} for x in calibrated]
    gaps=[{'from_minute':a['minute'],'to_minute':b['minute'],'gap_minutes':b['minute']-a['minute'],'within_limit':b['minute']-a['minute']<=10} for a,b in zip(readings,readings[1:])]
    coverage={'gaps':gaps,'end_minute':readings[-1]['minute'],'complete':readings[-1]['minute']>=30,'all_gaps_within_limit':all(g['within_limit'] for g in gaps)}
    events=[{'minute':x['minute'],'temp_tenths':x['temp_tenths']} for x in temps if not x['in_range']]
    reasons=[]
    if events: reasons.append('TEMPERATURE')
    if not coverage['all_gaps_within_limit']: reasons.append('GAP')
    if not coverage['complete']: reasons.append('COVERAGE')
    decision={'status':'HOLD' if reasons else 'RELEASE','reasons':reasons}
    names=['01_input.json','02_calibrated.json','03_temperature.json','04_coverage.json','05_events.json','06_decision.json']
    files={k:encode(v) for k,v in zip(names,[data,calibrated,temps,coverage,events,decision])}
    files['07_commitment.json']=encode({'sha256':{k:hashlib.sha256(v).hexdigest() for k,v in files.items()}})
    return files

def verify(files):
    expected=json.loads(files['07_commitment.json'])['sha256']
    return set(expected)==set(files)-{'07_commitment.json'} and all(hashlib.sha256(files[k]).hexdigest()==v for k,v in expected.items())

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--out',required=True); a=p.parse_args()
    data=json.loads(pathlib.Path(a.input).read_text()); files=build(data); out=pathlib.Path(a.out); out.mkdir(parents=True,exist_ok=False)
    for name,content in files.items(): (out/name).write_bytes(content)
    print(json.dumps({'artifacts':len(files),'integrity':verify(files),'status':'PASS'},sort_keys=True))
if __name__=='__main__': main()
