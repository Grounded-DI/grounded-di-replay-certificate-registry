#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def h(x): return hashlib.sha256(canon(x).encode()).hexdigest()
EXPECTED_SOURCE_BINDINGS={('REPORT-1', 'paragraph 4'): ('I reviewed the supplied synthetic imaging and pathology summaries. The claimant has the synthetic pulmonary diagnosis D-7 described in those records.', 'Dr. Mira Vale (synthetic expert)', None), ('REPORT-1', 'paragraph 7'): ('If the reported gasket handling involved asbestos-containing material, cumulative inhalation could have contributed to diagnosis D-7. I cannot identify a product, component, dose, or defendant from medical records alone.', 'Dr. Mira Vale (synthetic expert)', None), ('REPORT-1', 'paragraph 8'): ('The exposure was substantial and the dose was high enough to cause the condition.', 'Dr. Mira Vale (synthetic expert)', None), ('DEPO-1', 'page 88, lines 3-9'): ('Q. Did you calculate a cumulative dose? A. No. The supplied record contains no quantitative dose measurement, and I cannot estimate one from this material.', 'Dr. Mira Vale (synthetic expert)', 'Dr. Mira Vale'), ('DEPO-1', 'page 91, lines 12-18'): ('Q. So the exposure caused D-7? A. I said it could have contributed if the stated material and exposure assumptions are true. I cannot determine product identity or legal causation.', 'Dr. Mira Vale (synthetic expert)', 'Dr. Mira Vale'), ('WIT-1', 'page 24, lines 5-11'): ('I helped remove a gasket from a pump marked Model Q-4. I did not see a manufacturer label and cannot say what the gasket was made of.', 'Witness R (synthetic witness)', 'Witness R'), ('MED-1', 'record page 2'): ('Synthetic imaging and pathology summaries describe pulmonary diagnosis D-7. This summary does not identify a cause.', 'Synthetic record custodian', None), ('HIST-1', 'record page 1'): ('Synthetic history records prior smoking and a separate chronic pulmonary condition. The supplied record does not quantify their contribution to diagnosis D-7.', 'Synthetic record custodian', None), ('PROD-1', 'exhibit PX-1'): ('Model Q-4 pump delivered to North Plant; seller and manufacturer fields identify Acme Testworks.', 'Synthetic records custodian', None), ('WORK-1', 'exhibit PX-2'): ('A gasket was removed from a pump at North Plant. The entry does not identify the pump model, gasket supplier, or gasket material.', 'Synthetic records custodian', None), ('CONTROL-1', 'exhibit PX-3'): ('Diagnosis D-7 was documented after the reported work period. Temporal order alone does not state or establish causation.', 'Synthetic records custodian', None)}
def evaluate(d):
    src={(x["id"],x["location"]):x for x in d["sources"]}; rows=[]; issues=[]
    for s in d["sources"]:
        expected=EXPECTED_SOURCE_BINDINGS.get((s["id"],s["location"])); ok=bool((expected and (s.get("text"),s.get("author"),s.get("speaker"))==expected) or (s["id"].startswith("SUPPORT-") and bool(s.get("text")) and bool(s.get("location"))))
        rows.append({"record_id":"SOURCE:"+s["id"]+"@"+s["location"],"source_id":s["id"],"location":s["location"],"author_or_speaker":s.get("speaker") or s["author"],"source_fragment":s["text"],"exact_match":ok})
        if not ok: issues.append("source-record:"+s["id"]+"@"+s["location"])
    for o in d["opinions"]:
        x=src.get((o["source_id"],o["source_location"])); ok=bool(x and o["exact_opinion"] in x["text"])
        rows.append({"record_id":o["id"],"source_id":o["source_id"],"location":o["source_location"],"author_or_speaker":x.get("author") if x else None,"source_fragment":o["exact_opinion"],"exact_match":ok})
        if not ok: issues.append(o["id"])
    for (sid,loc),(text,author,speaker) in EXPECTED_SOURCE_BINDINGS.items():
        found=src.get((sid,loc))
        if not found or found.get("text")!=text or found.get("author")!=author or found.get("speaker")!=speaker: issues.append("source-record:"+sid+"@"+loc)
    for r in d["evidence_records"]:
        x=src.get((r["source_id"],next((s["location"] for s in d["sources"] if s["id"]==r["source_id"]),"")))
        ok=bool(x)
        rows.append({"record_id":r["id"],"source_id":r["source_id"],"location":x.get("location") if x else None,"author_or_speaker":x.get("author") if x else None,"source_fragment":x.get("text") if x else None,"exact_match":ok})
        if not ok: issues.append(r["id"])
    payload={"schema":"expertscope-sourcebinder-v1","matter_id":d["matter_id"],"bindings":rows,"binding_issues":issues,"status":"PASS" if not issues else "FAIL"}
    return dict(payload,canonical_record_sha256=h(payload))
if __name__=="__main__":
 d=json.loads(Path(sys.argv[1]).read_text()); r=evaluate(d); t=json.dumps(r,sort_keys=True,indent=2,ensure_ascii=False); print(t); Path(sys.argv[2]).write_text(t+"\n"); raise SystemExit(r["status"]!="PASS")
