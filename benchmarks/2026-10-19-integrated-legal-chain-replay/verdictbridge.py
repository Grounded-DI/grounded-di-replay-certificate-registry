#!/usr/bin/env python3
"""Synthetic VerdictBridge stage: guarded litigation-sufficiency synthesis."""
import hashlib
import json
import sys
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_payload(payload):
    return hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def verify_stage_hash(stage):
    payload = dict(stage)
    recorded = payload.pop("canonical_record_sha256", None)
    observed = sha256_payload(payload)
    return recorded == observed, recorded, observed


def main():
    if len(sys.argv) < 5:
        raise SystemExit("usage: verdictbridge.py INPUT.json BRIEFWISE.json DEPOBOT.json PIDBOT.json [OUTPUT.json]")
    input_path, brief_path, depo_path, pid_path = map(Path, sys.argv[1:5])
    output_path = Path(sys.argv[5]) if len(sys.argv) > 5 else None
    data = load(input_path)
    brief = load(brief_path)
    depo = load(depo_path)
    pid = load(pid_path)
    stage_records = {"briefwise": brief, "depobot": depo, "pidbot": pid}
    stage_integrity_failures = []
    verified_hashes = {}
    for name, stage in stage_records.items():
        valid, recorded, observed = verify_stage_hash(stage)
        verified_hashes[name] = recorded
        if not valid:
            stage_integrity_failures.append({"stage": name, "recorded": recorded, "observed": observed})

    pid_rows = {row["dimension"]: row for row in pid["evidence_matrix"]}
    authority_failure = bool(brief["unresolved"] or brief["unsupported"])
    source_failure = not depo["source_binding_valid"]
    product_failure = pid_rows["product_identification"]["support_state"] != "SUPPORTED"
    injection_present = bool(pid["unsupported_manual_injections"] or pid["unsupported_material_assertions"])
    unresolved_dimensions = [
        dimension for dimension in ("component_identification", "material_content", "exposure", "dose", "causation")
        if pid_rows[dimension]["support_state"] != "SUPPORTED"
    ]
    liability_failure = pid_rows["legal_liability"]["support_state"] != "SUPPORTED"
    contradiction_ids = [item["id"] for item in depo["findings"] if item["type"] == "DIRECT_CONTRADICTION"]

    if stage_integrity_failures or authority_failure or source_failure or product_failure or liability_failure:
        disposition = "INSUFFICIENT"
    elif injection_present or unresolved_dimensions or contradiction_ids:
        disposition = "REVIEW_REQUIRED"
    else:
        disposition = "VERDICT_READY"

    def element(element_name, support_state, basis, stage_result=None):
        result = {"element": element_name, "status": support_state, "basis": basis}
        if stage_result is not None:
            result["stage_result"] = stage_result
        return result

    authority_state = "UNRESOLVED" if authority_failure else "SUPPORTED"
    testimony_state = "UNRESOLVED" if source_failure else ("DISPUTED" if contradiction_ids else "SUPPORTED")
    elements = [
        element("jurisdiction_and_posture", "SUPPORTED", [data["jurisdiction"], data["procedural_posture"]]),
        element("authority_binding", authority_state, brief["unresolved"] + brief["unsupported"] or ["Required synthetic holdings are bound."]),
        element("testimony", testimony_state, contradiction_ids or ["The source-linked testimony matrix is preserved."]),
    ]
    for dimension in ("product_identification", "component_identification", "material_content", "worksite_chronology", "exposure", "dose", "causation", "legal_liability"):
        row = pid_rows[dimension]
        elements.append(element(dimension, row["support_state"], row["basis"], row["status"]))

    payload = {
        "schema": "verdictbridge-integrated-stage-v2",
        "matter_id": data["matter_id"],
        "stage": "VerdictBridge",
        "synthetic_fixture": True,
        "stage_hashes": verified_hashes,
        "stage_integrity_failures": stage_integrity_failures,
        "element_assessments": elements,
        "preserved_contradictions": contradiction_ids,
        "unresolved_evidence": [
            "Material content is not established by a manufacturer specification.",
            "Dose is not quantified.",
            "No causation opinion is supplied.",
            "The testimony contains a direct contradiction requiring credibility/foundation review.",
        ],
        "downstream_injection_result": "REJECTED" if injection_present else "NOT_PRESENT",
        "disposition": disposition,
        "verdict_ready": disposition == "VERDICT_READY",
        "cleanest_basis": (
            ["The synthetic record is insufficient because authority binding, source binding, or a required liability link failed."]
            if disposition == "INSUFFICIENT" else
            ["The synthetic record requires review because unresolved evidence remains before a verdict-ready disposition."]
            if disposition == "REVIEW_REQUIRED" else
            ["All disclosed synthetic gates passed."]
        ),
        "motion_recommendation": (
            "RESERVE — the synthetic record is insufficient for a supported final disposition; preserve the authority, testimony, product, material, dose, and causation gaps for review."
            if disposition == "INSUFFICIENT" else
            "RESERVE — unresolved synthetic evidence prevents a final sufficiency determination."
            if disposition == "REVIEW_REQUIRED" else
            "PROCEED — the supplied synthetic gate is satisfied."
        ),
        "measured_results_only": {
            "briefwise_stage_disposition": brief["stage_disposition"],
            "depobot_stage_disposition": depo["stage_disposition"],
            "pidbot_stage_disposition": pid["stage_disposition"],
            "contradiction_count": len(contradiction_ids),
            "unresolved_dimension_count": len(unresolved_dimensions),
            "upstream_hashes_verified": not stage_integrity_failures,
        },
        "inference_boundary": "Measured stage results are separated from legal or strategic inference.",
        "non_claims": [
            "No real legal correctness, filing readiness, product identification, exposure, dose, causation, liability, independent fresh-generation provenance, external verification, or production deployment is established."
        ],
    }
    result = dict(payload, final_chain_sha256=sha256_payload(payload))
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if output_path:
        output_path.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
