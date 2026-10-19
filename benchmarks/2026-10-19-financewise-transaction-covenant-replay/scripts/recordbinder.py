import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("input");p.add_argument("output");a=p.parse_args();d=json.loads(Path(a.input).read_text());bound=[];bad=[]
for k in ["bank_entries","invoices","payments","ledger_entries","ar","ap","debt","covenants"]:
 for r in d[k]:
  if r.get("source_id") and r.get("source_location"): bound.append({"record_id":r["id"],"source_id":r["source_id"],"source_location":r["source_location"],"source_fragment":json.dumps(r,sort_keys=True,separators=(",",":")),"date":r.get("date",r.get("issue_date")),"posting_date":r.get("posting_date"),"payment_date":r.get("date") if r.get("id","").startswith("PAY-") else None,"amount":r.get("amount",r.get("principal",r.get("current_portion"))),"currency":r.get("currency","USD"),"counterparty":r.get("counterparty"),"account":r.get("account",r.get("account_id"))})
  else: bad.append(r.get("id"))
out={"stage":"RecordBinder","input_sha256":hashlib.sha256(Path(a.input).read_bytes()).hexdigest(),"bound_record_count":len(bound),"rejected_record_ids":bad,"bindings":bound,"status":"PASS" if not bad else "REVIEW_REQUIRED"};Path(a.output).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n");print(json.dumps({"stage":out["stage"],"status":out["status"],"bound":len(bound)}))
