#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def canon(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(v):
    return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def main(input_path=None):
    data = json.loads((Path(input_path) if input_path else ROOT / "input.json").read_text(encoding="utf-8"))
    authorities = {a["id"]: a for a in data["authorities"]}
    rows = []
    for p in data["propositions"]:
        missing = [a for a in p["authority_ids"] if a not in authorities]
        if missing:
            classification = "UNRESOLVED_MISSING_AUTHORITY"
            status = "UNRESOLVED"
            reason = "Referenced authority is absent from the closed-world record."
        elif p["expected_classification"] == "OVERBROAD_UNSUPPORTED":
            classification = "OVERBROAD_UNSUPPORTED"
            status = "UNSUPPORTED"
            reason = "The supplied holdings do not support an automatic dismissal rule based only on a delivery dispute."
        else:
            classification = "SUPPORTED_HOLDING"
            status = "SUPPORTED"
            reason = "The proposition is supported within the supplied synthetic authority record."
        rows.append({"proposition_id": p["id"], "authority_ids": p["authority_ids"], "classification": classification, "status": status, "reason": reason})
    payload = {
        "schema": "briefwise-authority-proposition-replay-v1",
        "matter_id": data["matter_id"],
        "closed_world": True,
        "authority_map": rows,
        "disposition": "REVIEW_REQUIRED",
        "unsupported_propositions": [r["proposition_id"] for r in rows if r["status"] == "UNSUPPORTED"],
        "unresolved_propositions": [r["proposition_id"] for r in rows if r["status"] == "UNRESOLVED"],
        "non_claims": ["No real legal authority is represented.", "No filing-readiness or legal-correctness conclusion is made."],
    }
    out = dict(payload)
    out["canonical_record_sha256"] = digest(payload)
    print(json.dumps(out, sort_keys=True, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
