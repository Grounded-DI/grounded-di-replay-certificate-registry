import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("input");p.add_argument("run");a=p.parse_args();r=Path(a.run);f=json.loads((r/"final_chain.json").read_text());e=[]
if f.get("disposition")!="REVIEW_REQUIRED":e.append("wrong disposition")
if f.get("measured_ratio")!=4.0:e.append("wrong ratio")
if "MISSING-001" not in f.get("unresolved_items",[]):e.append("missing evidence collapsed")
if "B-001/INV-1001/AR-1001 conflict" not in f.get("unresolved_items",[]):e.append("conflict collapsed")
for x in ["recordbinder.json","transactionresolver.json","accountingboundary.json","covenantbridge.json"]:
 if not (r/x).exists():e.append("missing "+x)
out={"evaluator":"independent","imports_primary_stage_logic":False,"status":"PASS" if not e else "FAIL","errors":e,"final_chain_sha256":hashlib.sha256((r/"final_chain.json").read_bytes()).hexdigest()};print(json.dumps(out,sort_keys=True,indent=2));raise SystemExit(0 if not e else 1)
