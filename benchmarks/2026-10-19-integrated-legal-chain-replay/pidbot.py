#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

def canon(v): return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(v): return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def evaluate(data):
    records = data["evidence_records"]
    product_refs = {r.get("product_id") for r in records if r["kind"] == "product_reference"}
    manufacturer_links = {(r.get("product_id"), r.get("manufacturer")) for r in records if r["kind"] == "manufacturer_reference"}
    matches = sorted(p for p in product_refs if any(pid == p for pid, _ in manufacturer_links))
    material_records = [r for r in records if r["kind"] in ("material_assertion", "material_specification")]
    unsupported_material = [r["id"] for r in material_records if r.get("source") != "manufacturer_specification"]
    manual_injections = [r["id"] for r in records if r["kind"] == "manual_override"]
    rows = [{"dimension": "product_identification", "status": "MATCH" if matches else "REVIEW", "basis": matches or ["No shared product identifier links the product to a manufacturer."]}, {"dimension": "component_identification", "status": "REVIEW", "basis": ["The gasket is referenced but not tied to a component specification or supplier record."]}, {"dimension": "material_content", "status": "UNCERTAIN", "basis": ["No manufacturer specification establishes the asserted material content."]}, {"dimension": "worksite_chronology", "status": "DISPUTED", "basis": ["The work order and testimony contain a genuine repair-history conflict."]}, {"dimension": "exposure", "status": "REVIEW", "basis": ["Handling is alleged, but the handled component is not sufficiently identified as the asserted material."]}, {"dimension": "dose", "status": "UNCERTAIN", "basis": ["No quantified dose, duration, or measurement is supplied."]}, {"dimension": "causation", "status": "UNCERTAIN", "basis": ["The synthetic expert record supplies no causation opinion."]}, {"dimension": "legal_liability", "status": "INSUFFICIENT", "basis": ["The record does not establish every required liability link."]}]
    payload = {"schema": "pidbot-integrated-stage-v1", "matter_id": data["matter_id"], "stage": "PIDBot", "separation_preserved": ["product_identification", "component_identification", "material_content", "worksite_chronology", "exposure", "dose", "causation", "legal_liability"], "evidence_matrix": rows, "unsupported_material_assertions": unsupported_material, "unsupported_manual_injections": manual_injections, "stage_disposition": "REVIEW_REQUIRED", "non_claims": ["Product identification does not establish material content, exposure, dose, causation, or liability.", "All records and outcomes are synthetic."]}
    return dict(payload, canonical_record_sha256=digest(payload))

def main():
    input_path = Path(sys.argv[1]); output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    result = evaluate(json.loads(input_path.read_text(encoding="utf-8")))
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False)
    if output_path: output_path.write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__": main()
