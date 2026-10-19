#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def canon(v): return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(v): return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def evaluate(data):
    records = data["records"]
    product_refs = {r.get("product_id") for r in records if r["kind"] == "product_reference"}
    manufacturer_refs = {(r.get("product_id"), r.get("manufacturer")) for r in records if r["kind"] == "manufacturer_reference"}
    product_match = sorted(p for p in product_refs if any(pid == p for pid, _ in manufacturer_refs))
    rows = [
        {"dimension": "product_identification", "status": "MATCH" if product_match else "REVIEW", "basis": product_match or ["No shared product/manufacturer identifier."]},
        {"dimension": "component_identification", "status": "REVIEW", "basis": ["GASKET-UNSPECIFIED is referenced but not tied to a component manufacturer or specification."]},
        {"dimension": "material_content", "status": "UNCERTAIN", "basis": ["The only material statement is a witness belief; no product specification establishes content."]},
        {"dimension": "exposure", "status": "REVIEW", "basis": ["Handling is alleged, but the handled component is not sufficiently identified as the asserted material." ]},
        {"dimension": "dose", "status": "UNCERTAIN", "basis": ["No quantified dose, duration, or measurement is supplied."]},
        {"dimension": "causation", "status": "UNCERTAIN", "basis": ["The synthetic expert record supplies no causation opinion."]},
        {"dimension": "legal_liability", "status": "REVIEW", "basis": ["The record alleges liability but does not establish duty, breach, and causation."]},
    ]
    return rows

def main(input_path=None):
    data = json.loads((Path(input_path) if input_path else ROOT / "input.json").read_text())
    rows = evaluate(data)
    payload = {"schema": "pidbot-product-exposure-replay-v1", "matter_id": data["matter_id"], "closed_world": True, "separation_preserved": ["product_identification", "component_identification", "material_content", "exposure", "dose", "causation", "legal_liability"], "evidence_matrix": rows, "disposition": "REVIEW_REQUIRED", "non_claims": ["No product content, dose, causation, or legal liability is established.", "No real product, person, worksite, or medical conclusion is represented."]}
    print(json.dumps(dict(payload, canonical_record_sha256=digest(payload)), sort_keys=True, indent=2, ensure_ascii=False))

if __name__ == "__main__": main(sys.argv[1] if len(sys.argv) > 1 else None)
