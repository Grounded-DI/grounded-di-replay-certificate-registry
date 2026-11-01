#!/usr/bin/env python3
"""New, local public illustration. Not the historical DI² gate."""
import json,sys
from pathlib import Path

def write(path,obj):path.write_text(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n',encoding='utf-8')
class Gate:
    def __init__(self):self.bound={};self.used=set()
    def enroll(self,req):self.bound[req['id']]=req.copy()
    def dispatch(self,req,approved,now,provider):
        key=req['id']
        if key in self.used:return 'HELD'
        if not approved or key not in self.bound or self.bound[key]!=req or now>=req['expiry']:return 'DENIED'
        self.used.add(key)
        try:provider(req);return 'RELEASED'
        except TimeoutError:return 'UNKNOWN'
def request(identifier='op1',recipient='vendor-A',amount=12500):return {'id':identifier,'recipient':recipient,'amount':amount,'currency':'USD','expiry':200}
def main(out):
    out.mkdir(parents=True,exist_ok=False); log=out/'raw_effects.jsonl'; log.touch()
    events=[];results=[]
    def effect(case,req,loss=False):
        record={'case':case,'request_id':req['id'],'recipient':req['recipient'],'amount':req['amount'],'currency':req['currency']}
        with log.open('a',encoding='utf-8') as f:f.write(json.dumps(record,sort_keys=True,separators=(',',':'))+'\n')
        if loss:raise TimeoutError('simulated lost response')
    def case(name,scenario,expected):
        before=len(log.read_text().splitlines()); gate=Gate(); r=request();status=[]
        def send(q,approve=True,now=100,loss=False):
            s=gate.dispatch(q,approve,now,lambda x:effect(name,x,loss));status.append(s);events.append({'case':name,'id':q['id'],'approved':approve,'time':now,'result':s})
        if scenario=='baseline':
            for i in range(2):
                try:effect(name,r,True)
                except TimeoutError:status.append('UNKNOWN');events.append({'case':name,'id':r['id'],'result':'UNKNOWN','attempt':i+1})
        elif scenario=='approved':gate.enroll(r);send(r)
        elif scenario=='lost':gate.enroll(r);send(r,loss=True);send(r)
        elif scenario=='recipient':gate.enroll(r);send(request(recipient='vendor-B'))
        elif scenario=='amount':gate.enroll(r);send(request(amount=12501))
        elif scenario=='missing':gate.enroll(r);send(r,approve=False)
        elif scenario=='expired':gate.enroll(r);send(r,now=200)
        elif scenario=='new':
            gate.enroll(r);send(r);second=request('op2',amount=13000);gate.enroll(second);send(second)
        elif scenario=='new_id':
            gate.enroll(r);send(r,loss=True);second=request('op2');gate.enroll(second);send(second)
        observed={'status':status,'effects':len(log.read_text().splitlines())-before}
        if scenario=='lost':observed['lookup_count']=sum(1 for x in log.read_text().splitlines() if json.loads(x)['case']==name and json.loads(x)['request_id']=='op1')
        results.append({'case':name,'expected':expected,'observed':observed,'match':expected==observed})
    case('unprotected_loss','baseline',{'status':['UNKNOWN','UNKNOWN'],'effects':2})
    case('approved','approved',{'status':['RELEASED'],'effects':1})
    case('gated_loss','lost',{'status':['UNKNOWN','HELD'],'effects':1,'lookup_count':1})
    case('changed_recipient','recipient',{'status':['DENIED'],'effects':0})
    case('changed_amount','amount',{'status':['DENIED'],'effects':0})
    case('missing_approval','missing',{'status':['DENIED'],'effects':0})
    case('expired','expired',{'status':['DENIED'],'effects':0})
    case('distinct_new_action','new',{'status':['RELEASED','RELEASED'],'effects':2})
    case('duplicate_business_new_id','new_id',{'status':['UNKNOWN','RELEASED'],'effects':2})
    write(out/'results.json',results);write(out/'events.json',events);write(out/'effects.json',[json.loads(x) for x in log.read_text().splitlines()]);log.unlink()
    print(json.dumps({'cases':len(results),'matched':sum(x['match'] for x in results)}));return 0 if all(x['match'] for x in results) else 1
if __name__=='__main__':sys.exit(main(Path(sys.argv[1])))
