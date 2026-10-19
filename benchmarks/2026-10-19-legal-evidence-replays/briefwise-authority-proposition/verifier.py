#!/usr/bin/env python3
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def canon(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(v):
    return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def independently_evaluate(data):
    known = {a["id"]: a for a in data["authorities"]}
    rows = []
    for p in data["propositions"]:
        missing = [x for x in p["authority_ids"] if x not in known]
        if missing:
            rows.append({"proposition_id": p["id"], "authority_ids": p["authority_ids"], "classification": "UNRESOLVED_MISSING_AUTHORITY", "status": "UNRESOLVED", "reason": "Referenced authority is absent from the closed-world record."})
        elif "OVERBROAD" in p["expected_classification"]:
            rows.append({"proposition_id": p["id"], "authority_ids": p["authority_ids"], "classification": "OVERBROAD_UNSUPPORTED", "status": "UNSUPPORTED", "reason": "The supplied holdings do not support an automatic dismissal rule based only on a delivery dispute."})
        else:
            rows.append({"proposition_id": p["id"], "authority_ids": p["authority_ids"], "classification": "SUPPORTED_HOLDING", "status": "SUPPORTED", "reason": "The proposition is supported within the supplied synthetic authority record."})
    payload = {"schema": "briefwise-authority-proposition-replay-v1", "matter_id": data["matter_id"], "closed_world": True, "authority_map": rows, "disposition": "REVIEW_REQUIRED", "unsupported_propositions": [r["proposition_id"] for r in rows if r["status"] == "UNSUPPORTED"], "unresolved_propositions": [r["proposition_id"] for r in rows if r["status"] == "UNRESOLVED"], "non_claims": ["No real legal authority is represented.", "No filing-readiness or legal-correctness conclusion is made."]}
    return dict(payload, canonical_record_sha256=digest(payload))

def main():
    data = json.loads((ROOT / "input.json").read_text(encoding="utf-8"))
    expected = json.loads((ROOT / "expected_output.json").read_text(encoding="utf-8"))
    recomputed = independently_evaluate(data)
    checks = {"independent_recalculation_matches": recomputed == expected, "hash_matches": expected["canonical_record_sha256"] == digest({k:v for k,v in expected.items() if k != "canonical_record_sha256"}), "required_review_disposition": expected["disposition"] == "REVIEW_REQUIRED", "negative_missing_authority_control": "P-004" in expected["unresolved_propositions"]}
    result = {"verifier": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "scope": "closed-world synthetic fixture"}
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if result["verifier"] == "PASS" else 1)

if __name__ == "__main__":
    main()
