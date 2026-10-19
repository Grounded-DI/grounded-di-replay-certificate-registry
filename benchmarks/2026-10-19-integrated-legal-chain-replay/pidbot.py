#!/usr/bin/env python3
"""Synthetic PIDBot stage: product/exposure evidence separation."""
import hashlib
import json
import sys
from pathlib import Path

DIMENSIONS = [
    "product_identification",
    "component_identification",
    "material_content",
    "worksite_chronology",
    "exposure",
    "dose",
    "causation",
    "legal_liability",
]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_payload(payload):
    return hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest()


def evaluate(data):
    records = data["evidence_records"]
    complaint = data["complaint"]
    product_refs = [r for r in records if r.get("kind") == "product_reference"]
    manufacturer_refs = [r for r in records if r.get("kind") == "manufacturer_reference"]
    component_refs = [r for r in records if r.get("kind") == "component_reference"]
    material_records = [r for r in records if r.get("kind") in ("material_assertion", "material_specification")]
    exposure_records = [r for r in records if r.get("kind") == "exposure_assertion"]
    manual_injections = [r for r in records if r.get("kind") == "manual_override"]

    product_id = complaint["product_id"]
    defendant = complaint["defendant_candidate"]
    matching_product_ids = sorted({
        ref.get("product_id")
        for ref in product_refs
        if ref.get("product_id") == product_id
        and any(
            manufacturer.get("product_id") == product_id
            and manufacturer.get("manufacturer") == defendant
            for manufacturer in manufacturer_refs
        )
        and ref.get("worksite") == complaint["worksite"]
    })
    product_supported = bool(matching_product_ids)
    component_ids = sorted({
        ref.get("component")
        for ref in component_refs
        if ref.get("product_id") == product_id
        and ref.get("component") == complaint["component"]
    })
    material_specifications = [
        r for r in material_records
        if r.get("source") == "manufacturer_specification"
        and r.get("material") == complaint["alleged_material"]
        and r.get("component") == complaint["component"]
    ]
    unsupported_material = [
        r["id"] for r in material_records
        if r.get("source") != "manufacturer_specification"
    ]
    rows = [
        {
            "dimension": "product_identification",
            "status": "MATCH" if product_supported else "REVIEW",
            "support_state": "SUPPORTED" if product_supported else "UNRESOLVED",
            "evidence_ids": sorted({r["id"] for r in product_refs if r.get("product_id") == product_id} | {r["id"] for r in manufacturer_refs if r.get("product_id") == product_id}),
            "basis": matching_product_ids if product_supported else ["No disclosed product/worksite/manufacturer record satisfies the matching rule."],
        },
        {
            "dimension": "component_identification",
            "status": "REVIEW" if component_ids else "UNCERTAIN",
            "support_state": "UNRESOLVED",
            "evidence_ids": sorted(r["id"] for r in component_refs),
            "basis": ["The gasket is referenced but is not tied to a component specification or supplier record."],
        },
        {
            "dimension": "material_content",
            "status": "MATCH" if material_specifications else "UNCERTAIN",
            "support_state": "SUPPORTED" if material_specifications else "UNRESOLVED",
            "evidence_ids": [r["id"] for r in material_specifications] or unsupported_material,
            "basis": ["A manufacturer specification establishes the asserted material content."] if material_specifications else ["No manufacturer specification establishes the asserted material content; witness belief is not enough."],
        },
        {
            "dimension": "worksite_chronology",
            "status": "DISPUTED",
            "support_state": "DISPUTED",
            "evidence_ids": ["R-003", "R-005", "T-001", "T-002"],
            "basis": ["The work order and testimony contain a genuine repair-history conflict."],
        },
        {
            "dimension": "exposure",
            "status": "REVIEW",
            "support_state": "UNRESOLVED",
            "evidence_ids": [r["id"] for r in exposure_records],
            "basis": ["Handling is alleged, but the handled component is not sufficiently identified as the asserted material."],
        },
        {
            "dimension": "dose",
            "status": "UNCERTAIN",
            "support_state": "UNRESOLVED",
            "evidence_ids": [r["id"] for r in records if r.get("kind") == "dose_record"],
            "basis": ["No quantified dose, duration, or measurement is supplied."],
        },
        {
            "dimension": "causation",
            "status": "UNCERTAIN",
            "support_state": "UNRESOLVED",
            "evidence_ids": [r["id"] for r in records if r.get("kind") == "causation_record"],
            "basis": ["The synthetic expert record supplies no causation opinion."],
        },
        {
            "dimension": "legal_liability",
            "status": "INSUFFICIENT",
            "support_state": "UNSUPPORTED",
            "evidence_ids": [r["id"] for r in records if r.get("kind") == "liability_record"],
            "basis": ["The record does not establish every required liability link."],
        },
    ]
    payload = {
        "schema": "pidbot-integrated-stage-v2",
        "matter_id": data["matter_id"],
        "stage": "PIDBot",
        "synthetic_fixture": True,
        "separation_preserved": DIMENSIONS,
        "matching_rule": "product_id + defendant_candidate + manufacturer_record + complaint_worksite",
        "evidence_matrix": rows,
        "unsupported_material_assertions": unsupported_material,
        "unsupported_manual_injections": [r["id"] for r in manual_injections],
        "stage_disposition": "REVIEW_REQUIRED",
        "boundary_statement": "Product identification does not establish component identity, material content, exposure, dose, causation, or legal liability.",
        "non_claims": [
            "Product identification does not establish material content, exposure, dose, causation, or liability.",
            "All records and outcomes are synthetic.",
        ],
    }
    return dict(payload, canonical_record_sha256=sha256_payload(payload))


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: pidbot.py INPUT.json [OUTPUT.json]")
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    result = evaluate(json.loads(input_path.read_text(encoding="utf-8")))
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if output_path:
        output_path.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
