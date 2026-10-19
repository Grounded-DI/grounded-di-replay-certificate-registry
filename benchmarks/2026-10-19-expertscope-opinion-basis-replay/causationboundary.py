#!/usr/bin/env python3
import hashlib,json,sys
from pathlib import Path
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def h(x): return hashlib.sha256(canon(x).encode()).hexdigest()
def evaluate(d,op):
    rec={x["id"]:x for x in d["evidence_records"]}; statuses={x["id"]:x["status"] for x in d["evidence_records"]}; new_component=any(x["kind"]=="component_verified" and x["status"]=="present_verified" for x in d["evidence_records"]); new_material=any(x["kind"]=="material_test" and x["status"]=="present_verified" for x in d["evidence_records"]); new_dose=any(x["kind"]=="dose_measurement" and x["status"]=="present_verified" for x in d["evidence_records"])
    def row(dim,status,basis): return {"dimension":dim,"status":status,"basis":basis}
    product="SUPPORTED" if statuses.get("PROD-1")=="present" else "MISSING"
    component="SUPPORTED" if new_component else "UNRESOLVED"
    material="SUPPORTED" if new_material else "MISSING"
    exposure="SUPPORTED" if new_component and new_material and statuses.get("EXP-2")=="present_verified" else "DISPUTED"
    dose="SUPPORTED" if new_dose else "MISSING"
    diagnosis="SUPPORTED" if statuses.get("MED-1")=="present" else "MISSING"
    op2=next((x for x in op["opinions"] if x["opinion_id"]=="OP-2"),{}).get("assessment","UNRESOLVED")
    legal="UNRESOLVED"
    liability="UNRESOLVED"
    rows=[row("product_identity",product,["PROD-1"]),row("component_identity",component,["COMP-1" if not new_component else "COMP-2"]),row("material_content",material,["MAT-1" if not new_material else "MAT-2"]),row("exposure",exposure,["EXP-1" if not new_component else "EXP-2"]),row("dose",dose,["DOSE-1" if not new_dose else "DOSE-2"]),row("medical_diagnosis",diagnosis,["MED-1"]),row("expert_causation_opinion",op2,["OP-2"]),row("legal_causation",legal,["No legal-causation determination is supplied by this synthetic fixture."]),row("legal_liability",liability,["No liability determination is supplied by this synthetic fixture."])]
    if any(x["status"] in ("MISSING","DISPUTED","UNRESOLVED") for x in rows[:5]): disposition="INSUFFICIENT"
    else: disposition="REVIEW_REQUIRED" if legal=="UNRESOLVED" or op2!="SUPPORTED" else "VERDICT_READY"
    payload={"schema":"expertscope-causationboundary-v1","matter_id":d["matter_id"],"dimension_order":["product_identity","component_identity","material_content","exposure","dose","medical_diagnosis","expert_causation_opinion","legal_causation","legal_liability"],"evidence_matrix":rows,"negative_control":{"source_id":"CONTROL-1","classification":"TEMPORAL_SEQUENCE_ONLY_NOT_CAUSATION","affirmative_causation_proof":False},"disposition_gate":disposition}
    return dict(payload,canonical_record_sha256=h(payload))
if __name__=="__main__":
 d=json.loads(Path(sys.argv[1]).read_text()); o=json.loads(Path(sys.argv[2]).read_text()); r=evaluate(d,o); t=json.dumps(r,sort_keys=True,indent=2,ensure_ascii=False); print(t); Path(sys.argv[3]).write_text(t+"\n")
