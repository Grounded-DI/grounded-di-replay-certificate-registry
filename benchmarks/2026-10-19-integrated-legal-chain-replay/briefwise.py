#!/usr/bin/env python3
"""Synthetic BriefWise stage: authority/proposition binding."""
import hashlib
import json
import sys
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_payload(payload):
    return hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest()


def evaluate(data):
    authorities = {item["id"]: item for item in data["authorities"]}
    rows = []
    for proposition in data["legal_propositions"]:
        ids = proposition["authority_ids"]
        missing = [item for item in ids if item not in authorities]
        bound = []
        for authority_id in ids:
            authority = authorities.get(authority_id)
            if authority:
                bound.append({
                    "id": authority["id"],
                    "citation": authority["citation"],
                    "kind": authority["kind"],
                    "level": authority["level"],
                    "source_excerpt": authority["source_excerpt"],
                })
        if missing:
            classification = "UNRESOLVED_MISSING_AUTHORITY"
            support_state = "UNRESOLVED"
            reason = "A referenced synthetic authority is absent from the closed-world record."
        elif proposition["kind"] == "holding":
            classification = "SUPPORTED_HOLDING"
            support_state = "SUPPORTED"
            reason = "The supplied synthetic holding supports the proposition within the stated posture."
        elif proposition["kind"] == "dicta":
            classification = "DICTA_ONLY"
            support_state = "UNRESOLVED"
            reason = "The proposition is identified as dicta and is not treated as a necessary holding."
        elif proposition["kind"] == "inference":
            classification = "INFERENCE_REQUIRES_RECORD"
            support_state = "UNRESOLVED"
            reason = "The proposition requires application to the factual record and is not established by authority alone."
        else:
            classification = "UNSUPPORTED"
            support_state = "UNSUPPORTED"
            reason = "The proposition is not supported by the supplied closed-world authorities."
        rows.append({
            "proposition_id": proposition["id"],
            "text": proposition["text"],
            "kind": proposition["kind"],
            "authority_ids": ids,
            "bound_authorities": bound,
            "missing_authority_ids": missing,
            "classification": classification,
            "support_state": support_state,
            "reason": reason,
        })
    payload = {
        "schema": "briefwise-integrated-stage-v2",
        "matter_id": data["matter_id"],
        "stage": "BriefWise",
        "synthetic_fixture": True,
        "jurisdiction": data["jurisdiction"],
        "procedural_posture": data["procedural_posture"],
        "burden_and_standard": data["burden_and_standard"],
        "authority_map": rows,
        "stage_disposition": "REVIEW_REQUIRED" if any(x["support_state"] != "SUPPORTED" for x in rows) else "VERDICT_READY",
        "unresolved": [x["proposition_id"] for x in rows if x["support_state"] == "UNRESOLVED"],
        "unsupported": [x["proposition_id"] for x in rows if x["support_state"] == "UNSUPPORTED"],
        "inferences": [x["proposition_id"] for x in rows if x["classification"] == "INFERENCE_REQUIRES_RECORD"],
        "non_claims": [
            "Synthetic authorities only.",
            "Authority binding does not establish product identity, exposure, dose, causation, or liability.",
        ],
    }
    return dict(payload, canonical_record_sha256=sha256_payload(payload))


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: briefwise.py INPUT.json [OUTPUT.json]")
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    result = evaluate(json.loads(input_path.read_text(encoding="utf-8")))
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if output_path:
        output_path.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
