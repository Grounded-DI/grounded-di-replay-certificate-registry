#!/usr/bin/env python3
"""Independent verifier.

This file deliberately does not import any stage module. It recomputes the
canonical stage records from the fixture and then checks downstream hashes and
state transitions independently.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(payload):
    return hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest()


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def with_hash(payload, field="canonical_record_sha256"):
    return dict(payload, **{field: digest(payload)})


def expected_briefwise(data):
    authorities = {item["id"]: item for item in data["authorities"]}
    rows = []
    for proposition in data["legal_propositions"]:
        ids = proposition["authority_ids"]
        missing = [item for item in ids if item not in authorities]
        bound = []
        for authority_id in ids:
            authority = authorities.get(authority_id)
            if authority:
                bound.append({"id": authority["id"], "citation": authority["citation"], "kind": authority["kind"], "level": authority["level"], "source_excerpt": authority["source_excerpt"]})
        if missing:
            classification, support_state, reason = "UNRESOLVED_MISSING_AUTHORITY", "UNRESOLVED", "A referenced synthetic authority is absent from the closed-world record."
        elif proposition["kind"] == "holding":
            classification, support_state, reason = "SUPPORTED_HOLDING", "SUPPORTED", "The supplied synthetic holding supports the proposition within the stated posture."
        elif proposition["kind"] == "dicta":
            classification, support_state, reason = "DICTA_ONLY", "UNRESOLVED", "The proposition is identified as dicta and is not treated as a necessary holding."
        elif proposition["kind"] == "inference":
            classification, support_state, reason = "INFERENCE_REQUIRES_RECORD", "UNRESOLVED", "The proposition requires application to the factual record and is not established by authority alone."
        else:
            classification, support_state, reason = "UNSUPPORTED", "UNSUPPORTED", "The proposition is not supported by the supplied closed-world authorities."
        rows.append({"proposition_id": proposition["id"], "text": proposition["text"], "kind": proposition["kind"], "authority_ids": ids, "bound_authorities": bound, "missing_authority_ids": missing, "classification": classification, "support_state": support_state, "reason": reason})
    payload = {
        "schema": "briefwise-integrated-stage-v2", "matter_id": data["matter_id"], "stage": "BriefWise", "synthetic_fixture": True,
        "jurisdiction": data["jurisdiction"], "procedural_posture": data["procedural_posture"], "burden_and_standard": data["burden_and_standard"], "authority_map": rows,
        "stage_disposition": "REVIEW_REQUIRED" if any(x["support_state"] != "SUPPORTED" for x in rows) else "VERDICT_READY",
        "unresolved": [x["proposition_id"] for x in rows if x["support_state"] == "UNRESOLVED"],
        "unsupported": [x["proposition_id"] for x in rows if x["support_state"] == "UNSUPPORTED"],
        "inferences": [x["proposition_id"] for x in rows if x["classification"] == "INFERENCE_REQUIRES_RECORD"],
        "non_claims": ["Synthetic authorities only.", "Authority binding does not establish product identity, exposure, dose, causation, or liability."],
    }
    return with_hash(payload)


def expected_depobot(data):
    expected_bindings = {"T-001": "10:4-10:10", "T-002": "27:2-27:8", "T-003": "34:1-34:6", "T-004": "12:3-12:8", "T-005": "15:1-15:6", "T-006": "41:1-41:5", "T-007": "45:3-45:7"}
    transcript = {item["id"]: item for item in data["transcript"]}
    issues = []
    for entry_id, expected_page_line in expected_bindings.items():
        entry = transcript.get(entry_id)
        if entry is None:
            issues.append({"entry_id": entry_id, "reason": "missing_entry", "expected_page_line": expected_page_line})
        elif entry.get("page_line") != expected_page_line:
            issues.append({"entry_id": entry_id, "reason": "page_line_mismatch", "expected_page_line": expected_page_line, "observed_page_line": entry.get("page_line")})
    matrix = [{key: item[key] for key in ("id", "speaker", "question", "answer", "page_line", "exhibit", "source_fragment", "kind")} for item in data["transcript"]]
    first, second = transcript.get("T-001"), transcript.get("T-002")
    contradiction = bool(not issues and first and second and first.get("speaker") == second.get("speaker") == "Witness A" and "personally replaced" in first.get("answer", "").lower() and "did not perform any repair" in second.get("answer", "").lower() and "north plant" in first.get("answer", "").lower() and "north plant" in second.get("answer", "").lower() and "2014" in first.get("answer", "") and "2014" in second.get("answer", ""))
    findings = [
        {"id": "C-001", "type": "DIRECT_CONTRADICTION" if contradiction else ("UNRESOLVED_SOURCE_BINDING" if issues else "NOT_ESTABLISHED"), "entries": ["T-001", "T-002"], "speaker": "Witness A", "explanation": "The same witness gives opposite answers about the same repair at the same site and time." if contradiction else "The canonical source binding or same-event predicate is not established."},
        {"id": "C-002", "type": "AMBIGUITY", "entries": ["T-003"], "speaker": "Witness A", "explanation": "Probably gray plus lack of clear recollection is uncertainty, not contradiction."},
        {"id": "C-003", "type": "NEGATIVE_CONTROL_NOT_CONTRADICTION", "entries": ["T-004", "T-005"], "speaker": "Witness B", "explanation": "Lack of observation and inability to identify the repairer do not negate another witness's account."},
        {"id": "C-004", "type": "CHARACTERIZATION_NOT_ADMISSION", "entries": ["T-006"], "speaker": "Counsel", "explanation": "A characterized question without an answer is not an admission."},
        {"id": "C-005", "type": "OMISSION_MISSING_FOUNDATION", "entries": ["T-007"], "speaker": "Witness A", "explanation": "Failure to recall a manufacturer name does not establish an opposing fact."},
    ]
    payload = {"schema": "depobot-integrated-stage-v2", "matter_id": data["matter_id"], "stage": "DepoBot", "synthetic_fixture": True, "source_binding_valid": not issues, "binding_issues": issues, "testimony_matrix": matrix, "findings": findings, "stage_disposition": "REVIEW_REQUIRED", "unresolved": ["The contradiction may require credibility and foundation review."], "non_claims": ["No credibility determination is made.", "No synthetic testimony is treated as a real admission."]}
    return with_hash(payload)


def expected_pidbot(data):
    records, complaint = data["evidence_records"], data["complaint"]
    product_refs = [r for r in records if r.get("kind") == "product_reference"]
    manufacturer_refs = [r for r in records if r.get("kind") == "manufacturer_reference"]
    component_refs = [r for r in records if r.get("kind") == "component_reference"]
    material_records = [r for r in records if r.get("kind") in ("material_assertion", "material_specification")]
    exposure_records = [r for r in records if r.get("kind") == "exposure_assertion"]
    manual_injections = [r for r in records if r.get("kind") == "manual_override"]
    product_id, defendant = complaint["product_id"], complaint["defendant_candidate"]
    matching = sorted({ref.get("product_id") for ref in product_refs if ref.get("product_id") == product_id and any(m.get("product_id") == product_id and m.get("manufacturer") == defendant for m in manufacturer_refs) and ref.get("worksite") == complaint["worksite"]})
    component_ids = sorted({ref.get("component") for ref in component_refs if ref.get("product_id") == product_id and ref.get("component") == complaint["component"]})
    specs = [r for r in material_records if r.get("source") == "manufacturer_specification" and r.get("material") == complaint["alleged_material"] and r.get("component") == complaint["component"]]
    unsupported_material = [r["id"] for r in material_records if r.get("source") != "manufacturer_specification"]
    rows = [
        {"dimension": "product_identification", "status": "MATCH" if matching else "REVIEW", "support_state": "SUPPORTED" if matching else "UNRESOLVED", "evidence_ids": sorted({r["id"] for r in product_refs if r.get("product_id") == product_id} | {r["id"] for r in manufacturer_refs if r.get("product_id") == product_id}), "basis": matching if matching else ["No disclosed product/worksite/manufacturer record satisfies the matching rule."]},
        {"dimension": "component_identification", "status": "REVIEW" if component_ids else "UNCERTAIN", "support_state": "UNRESOLVED", "evidence_ids": sorted(r["id"] for r in component_refs), "basis": ["The gasket is referenced but is not tied to a component specification or supplier record."]},
        {"dimension": "material_content", "status": "MATCH" if specs else "UNCERTAIN", "support_state": "SUPPORTED" if specs else "UNRESOLVED", "evidence_ids": [r["id"] for r in specs] or unsupported_material, "basis": ["A manufacturer specification establishes the asserted material content."] if specs else ["No manufacturer specification establishes the asserted material content; witness belief is not enough."]},
        {"dimension": "worksite_chronology", "status": "DISPUTED", "support_state": "DISPUTED", "evidence_ids": ["R-003", "R-005", "T-001", "T-002"], "basis": ["The work order and testimony contain a genuine repair-history conflict."]},
        {"dimension": "exposure", "status": "REVIEW", "support_state": "UNRESOLVED", "evidence_ids": [r["id"] for r in exposure_records], "basis": ["Handling is alleged, but the handled component is not sufficiently identified as the asserted material."]},
        {"dimension": "dose", "status": "UNCERTAIN", "support_state": "UNRESOLVED", "evidence_ids": [r["id"] for r in records if r.get("kind") == "dose_record"], "basis": ["No quantified dose, duration, or measurement is supplied."]},
        {"dimension": "causation", "status": "UNCERTAIN", "support_state": "UNRESOLVED", "evidence_ids": [r["id"] for r in records if r.get("kind") == "causation_record"], "basis": ["The synthetic expert record supplies no causation opinion."]},
        {"dimension": "legal_liability", "status": "INSUFFICIENT", "support_state": "UNSUPPORTED", "evidence_ids": [r["id"] for r in records if r.get("kind") == "liability_record"], "basis": ["The record does not establish every required liability link."]},
    ]
    payload = {"schema": "pidbot-integrated-stage-v2", "matter_id": data["matter_id"], "stage": "PIDBot", "synthetic_fixture": True, "separation_preserved": ["product_identification", "component_identification", "material_content", "worksite_chronology", "exposure", "dose", "causation", "legal_liability"], "matching_rule": "product_id + defendant_candidate + manufacturer_record + complaint_worksite", "evidence_matrix": rows, "unsupported_material_assertions": unsupported_material, "unsupported_manual_injections": [r["id"] for r in manual_injections], "stage_disposition": "REVIEW_REQUIRED", "boundary_statement": "Product identification does not establish component identity, material content, exposure, dose, causation, or legal liability.", "non_claims": ["Product identification does not establish material content, exposure, dose, causation, or liability.", "All records and outcomes are synthetic."]}
    return with_hash(payload)


def verify_final(stage_records, final):
    checks = {}
    checks["final_hash_valid"] = final.get("final_chain_sha256") == digest({k: v for k, v in final.items() if k != "final_chain_sha256"})
    checks["final_stage_hashes_match"] = final.get("stage_hashes") == {name: stage.get("canonical_record_sha256") for name, stage in stage_records.items()}
    checks["upstream_integrity_failures_empty"] = final.get("stage_integrity_failures") == []
    brief, depo, pid = stage_records["briefwise"], stage_records["depobot"], stage_records["pidbot"]
    rows = {item["dimension"]: item for item in pid["evidence_matrix"]}
    authority_failure = bool(brief["unresolved"] or brief["unsupported"])
    source_failure = not depo["source_binding_valid"]
    product_failure = rows["product_identification"]["support_state"] != "SUPPORTED"
    liability_failure = rows["legal_liability"]["support_state"] != "SUPPORTED"
    injection_present = bool(pid["unsupported_manual_injections"] or pid["unsupported_material_assertions"])
    unresolved = [d for d in ("component_identification", "material_content", "exposure", "dose", "causation") if rows[d]["support_state"] != "SUPPORTED"]
    contradictions = [item["id"] for item in depo["findings"] if item["type"] == "DIRECT_CONTRADICTION"]
    if authority_failure or source_failure or product_failure or liability_failure:
        expected_disposition = "INSUFFICIENT"
    elif injection_present or unresolved or contradictions:
        expected_disposition = "REVIEW_REQUIRED"
    else:
        expected_disposition = "VERDICT_READY"
    checks["independent_disposition_rule"] = final.get("disposition") == expected_disposition
    checks["contradiction_preserved"] = final.get("preserved_contradictions") == contradictions
    checks["injection_not_upgraded"] = not (injection_present and final.get("verdict_ready"))
    checks["boundary_states_present"] = all(item.get("status") in {"SUPPORTED", "DISPUTED", "UNSUPPORTED", "UNRESOLVED"} for item in final.get("element_assessments", []))
    checks["exposure_not_causation"] = rows["exposure"]["support_state"] != "SUPPORTED" or rows["causation"]["support_state"] != "SUPPORTED"
    checks["dose_not_inferred"] = rows["dose"]["support_state"] != "SUPPORTED"
    return checks


def main():
    package = Path(__file__).resolve().parent
    run_dir = package / "run_1"
    if "--run-dir" in sys.argv:
        run_dir = Path(sys.argv[sys.argv.index("--run-dir") + 1]).resolve()
    expected_dir = package / "expected_stage_outputs"
    expected_final_path = package / "expected_final_chain.json"
    data = load(package / "input.json")
    recomputed = {"briefwise": expected_briefwise(data), "depobot": expected_depobot(data), "pidbot": expected_pidbot(data)}
    checks = {}
    for name, expected in recomputed.items():
        checks[f"independent_{name}_matches_expected"] = expected == load(expected_dir / f"{name}.json")
        checks[f"run_{name}_matches_independent"] = expected == load(run_dir / f"{name}.json")
        checks[f"run_{name}_hash_valid"] = expected["canonical_record_sha256"] == load(run_dir / f"{name}.json")["canonical_record_sha256"]
    final = load(run_dir / "final_chain.json")
    expected_final = load(expected_final_path)
    checks["run_final_matches_expected"] = final == expected_final if run_dir == package / "run_1" else False
    checks.update({f"final_{key}": value for key, value in verify_final(recomputed, final).items()})
    if (package / "run_2").exists() and run_dir == package / "run_1":
        checks["two_fresh_runs_have_identical_canonical_outputs"] = all(load(package / "run_1" / f"{name}.json") == load(package / "run_2" / f"{name}.json") for name in ("briefwise", "depobot", "pidbot", "final_chain"))
    else:
        checks["two_fresh_runs_have_identical_canonical_outputs"] = False
    checks["negative_control_is_preserved"] = any(item["type"] == "NEGATIVE_CONTROL_NOT_CONTRADICTION" for item in recomputed["depobot"]["findings"])
    checks["stage_execution_receipts_present"] = (run_dir / "execution.json").exists() and all((run_dir / f"{label}.{suffix}.txt").exists() for label in ("briefwise", "depobot", "pidbot", "verdictbridge") for suffix in ("stdout", "stderr"))
    result = {"verifier": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "scope": "closed-world synthetic integrated chain", "python": sys.version.split()[0], "platform": platform.platform(), "run_dir": str(run_dir)}
    print(json.dumps(result, sort_keys=True, indent=2))
    if "--run-dir" not in sys.argv:
        (package / "independent_evaluator_result.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    raise SystemExit(0 if result["verifier"] == "PASS" else 1)


if __name__ == "__main__":
    main()
