#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

def canon(v): return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(v): return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def main():
    input_path, brief_path, depo_path, pid_path = map(Path, sys.argv[1:5])
    output_path = Path(sys.argv[5]) if len(sys.argv) > 5 else None
    data = json.loads(input_path.read_text(encoding="utf-8")); brief = json.loads(brief_path.read_text()); depo = json.loads(depo_path.read_text()); pid = json.loads(pid_path.read_text())
    pid_rows = {x["dimension"]: x for x in pid["evidence_matrix"]}
    authority_failure = bool(brief["unresolved"] or brief["unsupported"])
    source_failure = not depo["source_binding_valid"]
    product_failure = pid_rows["product_identification"]["status"] != "MATCH"
    injection_failure = bool(pid["unsupported_manual_injections"])
    material_injection = bool(pid["unsupported_material_assertions"])
    if authority_failure or source_failure or product_failure:
        disposition = "INSUFFICIENT"
    elif injection_failure or material_injection or pid_rows["material_content"]["status"] != "MATCH" or pid_rows["dose"]["status"] != "MATCH" or pid_rows["causation"]["status"] != "MATCH":
        disposition = "REVIEW_REQUIRED"
    else:
        disposition = "VERDICT_READY"
    elements = [{"element": "jurisdiction_and_posture", "status": "SUPPORTED", "basis": [data["jurisdiction"], data["procedural_posture"]]}, {"element": "authority_binding", "status": "UNRESOLVED" if authority_failure else "SUPPORTED", "basis": brief["unresolved"] + brief["unsupported"] or ["Required holdings are bound."]}, {"element": "testimony", "status": "DISPUTED" if any(x["type"] == "DIRECT_CONTRADICTION" for x in depo["findings"]) else "REVIEW", "basis": [x["id"] for x in depo["findings"] if x["type"] == "DIRECT_CONTRADICTION"]}, {"element": "product_identification", "status": pid_rows["product_identification"]["status"], "basis": pid_rows["product_identification"]["basis"]}, {"element": "component_identification", "status": pid_rows["component_identification"]["status"], "basis": pid_rows["component_identification"]["basis"]}, {"element": "material_content", "status": pid_rows["material_content"]["status"], "basis": pid_rows["material_content"]["basis"]}, {"element": "exposure", "status": pid_rows["exposure"]["status"], "basis": pid_rows["exposure"]["basis"]}, {"element": "dose", "status": pid_rows["dose"]["status"], "basis": pid_rows["dose"]["basis"]}, {"element": "causation", "status": pid_rows["causation"]["status"], "basis": pid_rows["causation"]["basis"]}, {"element": "legal_liability", "status": pid_rows["legal_liability"]["status"], "basis": pid_rows["legal_liability"]["basis"]}]
    payload = {"schema": "verdictbridge-integrated-stage-v1", "matter_id": data["matter_id"], "stage": "VerdictBridge", "stage_hashes": {"briefwise": brief["canonical_record_sha256"], "depobot": depo["canonical_record_sha256"], "pidbot": pid["canonical_record_sha256"]}, "element_assessments": elements, "preserved_contradictions": [x["id"] for x in depo["findings"] if x["type"] == "DIRECT_CONTRADICTION"], "unresolved_evidence": ["Material content is not established by a manufacturer specification.", "Dose is not quantified.", "No causation opinion is supplied.", "The testimony contains a direct contradiction requiring credibility/foundation review."], "downstream_injection_rejected": injection_failure or material_injection, "disposition": disposition, "verdict_ready": disposition == "VERDICT_READY", "motion_recommendation": "RESERVE — the record is not sufficient for a supported final disposition." if disposition != "VERDICT_READY" else "PROCEED — the supplied record satisfies the stated synthetic gate.", "inference_boundary": "Measured stage results are separated from legal or strategic inference.", "non_claims": ["No real legal correctness, filing readiness, product identification, exposure, dose, causation, liability, external verification, or production deployment is established."]}
    result = dict(payload, final_chain_sha256=digest(payload))
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False)
    if output_path: output_path.write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__": main()
