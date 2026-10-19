#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def h(x): return hashlib.sha256(canon(x).encode()).hexdigest()
def main():
 d=json.loads(Path(sys.argv[1]).read_text()); b=json.loads(Path(sys.argv[2]).read_text()); o=json.loads(Path(sys.argv[3]).read_text()); c=json.loads(Path(sys.argv[4]).read_text()); out=Path(sys.argv[5]); valid=all(x.get("matter_id")==d["matter_id"] for x in (b,o,c)) and b["canonical_record_sha256"]==h({k:v for k,v in b.items() if k!="canonical_record_sha256"}) and o["canonical_record_sha256"]==h({k:v for k,v in o.items() if k!="canonical_record_sha256"}) and c["canonical_record_sha256"]==h({k:v for k,v in c.items() if k!="canonical_record_sha256"}) and b["status"]=="PASS"
 if not valid: disp="INSUFFICIENT"
 else: disp=c["disposition_gate"]
 rows=c["evidence_matrix"]
 payload={"schema":"expertscope-verdictbridge-v1","matter_id":d["matter_id"],"upstream_hashes":{"sourcebinder":b["canonical_record_sha256"],"opinionmapper":o["canonical_record_sha256"],"causationboundary":c["canonical_record_sha256"]},"chain_valid":valid,"preserved_opinions":[{"id":x["opinion_id"],"assessment":x["assessment"],"exact_opinion":x["exact_opinion"],"limitations":x["limitations"]} for x in o["opinions"]],"preserved_negative_control":c["negative_control"],"element_statuses":rows,"disposition":disp,"motion_assessment":"RESERVE for record development: component/material linkage, exposure foundation, dose, and legal causation remain unresolved in this fixture.","measured_results_vs_inference":"Stage statuses and hashes are measured from this fixture; the motion assessment is a synthetic rule-based inference.","unresolved":[x["dimension"] for x in rows if x["status"] in ("MISSING","DISPUTED","UNRESOLVED","QUALIFIED")],"non_claims":["No real legal, admissibility, clinical, medical-causation, legal-causation, liability, filing-readiness, external-verification, or deployment conclusion is made."]}
 result=dict(payload,final_chain_sha256=h(payload)); text=json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False); print(text); out.write_text(text+"\n"); raise SystemExit(0 if valid else 2)
if __name__=="__main__": main()
