#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

def canon(v): return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(v): return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def evaluate(data):
    authorities = {a["id"]: a for a in data["authorities"]}
    rows = []
    for p in data["legal_propositions"]:
        missing = [x for x in p["authority_ids"] if x not in authorities]
        if missing:
            classification, status, reason = "UNRESOLVED_MISSING_AUTHORITY", "UNRESOLVED", "A referenced authority is absent from the closed-world record."
        elif p["kind"] == "holding":
            classification, status, reason = "SUPPORTED_HOLDING", "SUPPORTED", "The supplied synthetic holding supports the proposition within the stated posture."
        elif p["kind"] == "dicta":
            classification, status, reason = "DICTA_ONLY", "LIMITED", "The proposition is not a necessary holding in the supplied record."
        elif p["kind"] == "inference":
            classification, status, reason = "INFERENCE_REQUIRES_RECORD", "INFERENCE", "The proposition requires application to the factual record and is not established by authority alone."
        else:
            classification, status, reason = "UNSUPPORTED", "UNSUPPORTED", "The proposition is not supported by the supplied closed-world authorities."
        rows.append({"proposition_id": p["id"], "authority_ids": p["authority_ids"], "classification": classification, "status": status, "reason": reason})
    payload = {"schema": "briefwise-integrated-stage-v1", "matter_id": data["matter_id"], "stage": "BriefWise", "jurisdiction": data["jurisdiction"], "procedural_posture": data["procedural_posture"], "burden_and_standard": data["burden_and_standard"], "authority_map": rows, "stage_disposition": "REVIEW_REQUIRED", "unresolved": [x["proposition_id"] for x in rows if x["status"] == "UNRESOLVED"], "unsupported": [x["proposition_id"] for x in rows if x["status"] == "UNSUPPORTED"], "inferences": [x["proposition_id"] for x in rows if x["status"] == "INFERENCE"], "non_claims": ["Synthetic authorities only.", "Authority binding does not establish product identity, exposure, dose, causation, or liability."]}
    return dict(payload, canonical_record_sha256=digest(payload))

def main():
    input_path = Path(sys.argv[1]); output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    result = evaluate(json.loads(input_path.read_text(encoding="utf-8")))
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False)
    if output_path: output_path.write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__": main()
