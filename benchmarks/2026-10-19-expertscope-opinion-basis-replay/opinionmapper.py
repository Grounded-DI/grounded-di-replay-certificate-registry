#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def h(x): return hashlib.sha256(canon(x).encode()).hexdigest()
def evaluate(d,binder):
    records={r["id"]:r for r in d["evidence_records"]}; bindings={x["record_id"]:x for x in binder["bindings"]}; rows=[]
    for o in d["opinions"]:
        bind=bindings.get(o["id"],{}); ass=[]
        for a in o["assumptions"]:
            refs=[records.get(i) for i in a["evidence_refs"]]; statuses=[]
            for r in refs:
                if r is None: statuses.append("MISSING")
                elif r.get("status") in ("present",): statuses.append("SUPPORTED")
                elif r.get("status")=="present_but_unlinked": statuses.append("UNRESOLVED")
                elif r.get("status")=="lay_report_unverified": statuses.append("DISPUTED")
                elif r.get("status")=="explicitly_unquantified": statuses.append("MISSING")
                elif r.get("status")=="present_verified": statuses.append("SUPPORTED")
                else: statuses.append("UNRESOLVED")
            status="SUPPORTED" if statuses and all(s=="SUPPORTED" for s in statuses) else ("DISPUTED" if "DISPUTED" in statuses else ("MISSING" if "MISSING" in statuses else "UNRESOLVED"))
            ass.append({"assumption_id":a["id"],"text":a["text"],"evidence_refs":a["evidence_refs"],"status":status})
        source_ok=bind.get("exact_match",False)
        if not source_ok: result="UNRESOLVED"
        elif o["id"]=="OP-1" and all(a["status"]=="SUPPORTED" for a in ass): result="SUPPORTED"
        elif o["id"]=="OP-2": result="QUALIFIED" if any(a["status"]!="SUPPORTED" for a in ass) else "SUPPORTED"
        elif o["id"]=="OP-3": result="UNSUPPORTED"
        else: result="UNRESOLVED"
        rows.append({"opinion_id":o["id"],"exact_opinion":o["exact_opinion"],"source":{"id":o["source_id"],"location":o["source_location"],"source_fragment":bind.get("source_fragment"),"exact_match":source_ok},"stated_basis":o["basis"],"method":o["method"],"assumptions":ass,"scope":o["scope"],"limitations":o["limitations"],"assessment":result})
    payload={"schema":"expertscope-opinionmapper-v1","matter_id":d["matter_id"],"opinions":rows,"counts":{k:sum(x["assessment"]==k for x in rows) for k in ["SUPPORTED","QUALIFIED","UNSUPPORTED","UNRESOLVED"]}}
    return dict(payload,canonical_record_sha256=h(payload))
if __name__=="__main__":
 d=json.loads(Path(sys.argv[1]).read_text()); b=json.loads(Path(sys.argv[2]).read_text()); r=evaluate(d,b); t=json.dumps(r,sort_keys=True,indent=2,ensure_ascii=False); print(t); Path(sys.argv[3]).write_text(t+"\n")
