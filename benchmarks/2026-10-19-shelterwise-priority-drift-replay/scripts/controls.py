#!/usr/bin/env python3
"""Run real ShelterWise mutated-input and downstream-tamper controls."""

import argparse
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

from common import file_sha256, load_json, write_json


def add_source(data, source):
    data.setdefault("sources", []).append(source)


def update_source_and_record(data, source_id, fragment):
    for source in data.get("sources", []):
        if source.get("source_id") == source_id:
            source["exact_source_fragment"] = fragment
    for record in data.get("intake_records", []):
        if record.get("source_id") == source_id:
            record["exact_source_fragment"] = fragment
    for record in data.get("inventory", {}).get("resource_records", []):
        if record.get("source_id") == source_id:
            record["exact_source_fragment"] = fragment
    for record in data.get("inventory", {}).get("reservations", []):
        if record.get("source_id") == source_id:
            record["exact_source_fragment"] = fragment
    for record in data.get("rules", []):
        if record.get("source_id") == source_id:
            record["exact_source_fragment"] = fragment
    for record in data.get("negative_control_memos", []):
        if record.get("source_id") == source_id:
            record["exact_source_fragment"] = fragment


def add_supporting_intake(data, record, source):
    add_source(data, source)
    data.setdefault("intake_records", []).append(record)


def mutate(data, name):
    d = copy.deepcopy(data)
    if name == "confirmed_safety_to_unverified":
        record = next(item for item in d["intake_records"] if item["record_id"] == "INT-H001-SAFETY")
        record["status"] = "UNVERIFIED"
        update_source_and_record(d, "SRC-INT-H001", "Synthetic intake H-001: immediate safety need reported; need remains unverified.")
    elif name == "accessibility_need_removed":
        d["intake_records"] = [item for item in d["intake_records"] if item["record_id"] != "INT-H006-ACCESS"]
        d["sources"] = [item for item in d["sources"] if item["source_id"] != "SRC-INT-H006"]
    elif name == "capacity_reduced_below_demand":
        resource = next(item for item in d["inventory"]["resource_records"] if item["resource_id"] == "COT-STD-003")
        resource["capacity"] = 0
        update_source_and_record(d, "SRC-INV-003", "Synthetic inventory row 3: COT-STD-003 has zero standard cots.")
    elif name == "duplicate_resource_reservation":
        add_source(d, {"source_id": "SRC-RES-008", "source_type": "reservation", "source_location": "reservation ledger row 8", "exact_source_fragment": "Synthetic reservation row 8: COT-STD-001 reserved for H-006."})
        d["inventory"]["reservations"].append({"reservation_id": "RES-008", "resource_id": "COT-STD-001", "household_id": "H-006", "quantity": 1, "status": "ACTIVE", "source_id": "SRC-RES-008", "source_location": "reservation ledger row 8", "exact_source_fragment": "Synthetic reservation row 8: COT-STD-001 reserved for H-006."})
    elif name == "duplicate_household":
        duplicate = copy.deepcopy(next(item for item in d["household_profiles"] if item["household_id"] == "H-003"))
        duplicate["household_id"] = "H-003-DUP"
        duplicate["display_label"] = "Household Duplicate Fixture"
        duplicate["duplicate_key"] = "FP-003"
        d["household_profiles"].append(duplicate)
    elif name == "stale_record_newer_without_matching_authority":
        add_source(d, {"source_id": "SRC-RULE-STALE", "source_type": "rulebook", "source_location": "untrusted memo page 1", "priority_level": 0, "exact_source_fragment": "Synthetic untrusted memo: immediate safety is convenience priority 0."})
        d["rules"].append({"rule_id": "R-STALE-001", "authority_key": "untrusted.memo", "subject": "immediate safety priority", "issued_at": "2026-10-19T08:00:00Z", "effective_date": "2026-10-19", "applicable_period": {"start": "2026-10-19T00:00:00Z", "end": "2026-10-20T00:00:00Z"}, "priority_level": 0, "source_id": "SRC-RULE-STALE", "source_location": "untrusted memo page 1", "exact_source_fragment": "Synthetic untrusted memo: immediate safety is convenience priority 0.", "text": "Immediate safety is convenience priority 0.", "status": "ACTIVE"})
    elif name == "unauthorized_priority_rule_added":
        add_source(d, {"source_id": "SRC-RULE-UNAUTHORIZED", "source_type": "rulebook", "source_location": "unapproved flyer page 1", "priority_level": 0, "exact_source_fragment": "Synthetic unapproved flyer: labels control priority 0."})
        d["rules"].append({"rule_id": "R-UNAUTHORIZED-001", "authority_key": "unapproved.flyer", "subject": "identity priority", "issued_at": "2026-10-19T08:05:00Z", "effective_date": "2026-10-19", "applicable_period": {"start": "2026-10-19T00:00:00Z", "end": "2026-10-20T00:00:00Z"}, "priority_level": 0, "source_id": "SRC-RULE-UNAUTHORIZED", "source_location": "unapproved flyer page 1", "exact_source_fragment": "Synthetic unapproved flyer: labels control priority 0.", "text": "Household labels control priority.", "status": "ACTIVE"})
    elif name == "negative_control_memo_altered":
        update_source_and_record(d, "SRC-MEMO-001", "Synthetic negative-control memo: an altered dramatic claim says the largest household receives every resource immediately.")
        d["negative_control_memos"][0]["text"] = "An altered dramatic claim says the largest household receives every resource immediately."
    elif name == "labels_permuted":
        labels = {item["household_id"]: item.get("display_label") for item in d["household_profiles"]}
        d["household_profiles"][0]["display_label"] = labels["H-006"]
        d["household_profiles"][-1]["display_label"] = labels["H-001"]
    elif name == "downstream_assignment_injection":
        d["injected_assignments"] = [{"household_id": "H-004", "resource_id": "TRANS-001", "status": "ASSIGNABLE", "source": "downstream label only"}]
    elif name == "supporting_new_confirmation":
        add_supporting_intake(d, {"record_id": "INT-H004-SUPPORT", "household_id": "H-004", "need_type": "transport", "value": "transport_seat_requested", "status": "CONFIRMED", "timestamp": "2026-10-19T08:10:00Z", "speaker_or_source": "synthetic intake desk", "applicable_period": {"start": "2026-10-19T00:00:00Z", "end": "2026-10-20T00:00:00Z"}, "source_id": "SRC-INT-H004-SUPPORT", "source_location": "intake H-004 line 2", "exact_source_fragment": "Synthetic intake H-004: transport seat need confirmed by a supporting intake record."}, {"source_id": "SRC-INT-H004-SUPPORT", "source_type": "supporting_intake", "source_location": "intake H-004 line 2", "exact_source_fragment": "Synthetic intake H-004: transport seat need confirmed by a supporting intake record."})
    elif name == "conclusory_assertion_only":
        add_supporting_intake(d, {"record_id": "INT-H004-CONCLUSION", "household_id": "H-004", "need_type": "transport", "value": "transport_seat_requested", "status": "CONFIRMED", "timestamp": "2026-10-19T08:11:00Z", "speaker_or_source": "synthetic reviewer memo", "applicable_period": {"start": "2026-10-19T00:00:00Z", "end": "2026-10-20T00:00:00Z"}, "source_id": "SRC-INT-H004-CONCLUSION", "source_location": "review memo paragraph 1", "exact_source_fragment": "Synthetic reviewer memo concludes transport is confirmed without underlying record."}, {"source_id": "SRC-INT-H004-CONCLUSION", "source_type": "negative_control_memo", "source_location": "review memo paragraph 1", "exact_source_fragment": "Synthetic reviewer memo concludes transport is confirmed without underlying record."})
    elif name == "unsupported_confirmation":
        record = next(item for item in d["intake_records"] if item["record_id"] == "INT-H004-TRANS")
        record["status"] = "CONFIRMED"
    elif name == "priority_inversion":
        rule = next(item for item in d["rules"] if item["rule_id"] == "R-SAFETY")
        rule["priority_level"] = 9
    elif name == "missing_evidence_collapse":
        record = next(item for item in d["intake_records"] if item["record_id"] == "INT-H004-TRANS")
        record["status"] = "CONFIRMED"
        update_source_and_record(d, "SRC-INT-H004", "Synthetic intake H-004: transport seat need confirmed by relabeled existing record.")
    else:
        raise ValueError(name)
    return d


def run_case(case_dir, input_path, pipeline, package_root, baseline_input, baseline_run):
    output_dir = case_dir / "run"
    command = [sys.executable, str(pipeline), str(input_path), str(output_dir), "--baseline-input", str(baseline_input), "--baseline-run", str(baseline_run)]
    process = subprocess.run(command, cwd=package_root, text=True, capture_output=True, check=False)
    (case_dir / "pipeline.stdout.txt").write_text(process.stdout, encoding="utf-8")
    (case_dir / "pipeline.stderr.txt").write_text(process.stderr, encoding="utf-8")
    return process, output_dir, command


def output_summary(output_dir):
    final = load_json(output_dir / "final_chain.json")
    allocation = load_json(output_dir / "allocationbridge.json")
    intake = load_json(output_dir / "intakebinder.json")
    capacity = load_json(output_dir / "capacityledger.json")
    rules = load_json(output_dir / "rulebinder.json")
    return {"disposition": final.get("disposition"), "households": final.get("household_dispositions"), "drift_events": final.get("drift_events"), "intake_errors": [item.get("kind") for item in intake.get("errors", [])], "rule_errors": [item.get("kind") for item in rules.get("errors", [])], "duplicate_reservations": [item.get("resource_id") for item in capacity.get("duplicate_reservations", [])], "allocation": allocation.get("allocation_records")}


def household(summary, household_id):
    return next(item for item in summary["households"] if item["household_id"] == household_id)


def need_record(summary, household_id, need_id):
    record = next(item for item in summary["allocation"] if item["household_id"] == household_id)
    return next(item for item in record["assignments"] if item["need_id"] == need_id)


def assert_case(name, baseline_summary, result_summary, rules, intake, capacity, final):
    baseline_households = {item["household_id"]: item for item in baseline_summary["households"]}
    current_households = {item["household_id"]: item for item in result_summary["households"]}
    if name == "confirmed_safety_to_unverified":
        return household(result_summary, "H-001")["disposition"] == "REVIEW_REQUIRED" and household(result_summary, "H-001")["priority_level"] > baseline_households["H-001"]["priority_level"], "confirmed safety downgrade changed priority and assignment"
    if name == "accessibility_need_removed":
        return household(result_summary, "H-006")["disposition"] == "INSUFFICIENT_RECORD" and any(item.get("status") == "MISSING" for item in intake["households"][-1]["needs"]), "removed accessibility evidence became missing"
    if name == "capacity_reduced_below_demand":
        return need_record(result_summary, "H-003", "NEED-H003-COTS")["status"] == "NO_FEASIBLE_ASSIGNMENT" and need_record(result_summary, "H-003", "NEED-H003-COTS")["unmet_need"] > 0, "cot demand exceeded altered capacity"
    if name == "duplicate_resource_reservation":
        return "COT-STD-001" in result_summary["duplicate_reservations"] and household(result_summary, "H-001")["disposition"] == "REVIEW_REQUIRED", "duplicate reservation produced a capacity conflict"
    if name == "duplicate_household":
        return any(sorted(item["household_ids"]) == ["H-003", "H-003-DUP"] for item in intake.get("duplicate_household_candidates", [])) and "H-003-DUP" in current_households, "duplicate household candidate preserved"
    if name in {"stale_record_newer_without_matching_authority", "unauthorized_priority_rule_added"}:
        return "UNAUTHORIZED_RULE_CHANGE" in result_summary["rule_errors"] and rules.get("active_rule_ids") == ["R-SAFETY", "R-ACCESS", "R-FAMILY", "R-UNIQUE", "R-UNCERTAIN", "R-SUPERSESSION", "R-NEUTRAL"], "unauthorized rule did not enter active rule set"
    if name == "negative_control_memo_altered":
        return result_summary["households"] == baseline_summary["households"] and result_summary["disposition"] == baseline_summary["disposition"], "altered negative-control memo did not affect allocation"
    if name == "labels_permuted":
        return result_summary["households"] == baseline_summary["households"] and result_summary["allocation"] == baseline_summary["allocation"], "display labels did not affect decisions"
    if name == "downstream_assignment_injection":
        return "DOWNSTREAM_ASSIGNMENT_INJECTION" in result_summary["drift_events"] and result_summary["households"] == baseline_summary["households"], "injected downstream assignment was ignored and flagged"
    if name == "supporting_new_confirmation":
        return household(result_summary, "H-004")["disposition"] == "ASSIGNABLE", "new source-supported confirmation changed H-004 to assignable"
    if name == "conclusory_assertion_only":
        return household(result_summary, "H-004")["disposition"] == "REVIEW_REQUIRED" and "UNAUTHORIZED_SOURCE_TYPE" in result_summary["intake_errors"], "conclusory memo did not establish a need"
    if name == "unsupported_confirmation":
        return household(result_summary, "H-004")["disposition"] == "REVIEW_REQUIRED" and "UNSUPPORTED_CONFIRMATION" in result_summary["intake_errors"], "status-only confirmation was rejected"
    if name == "priority_inversion":
        return "PRIORITY_INVERSION" in result_summary["drift_events"] and "RULE_PRIORITY_SOURCE_MISMATCH" in result_summary["rule_errors"], "priority inversion was detected from source mismatch"
    if name == "missing_evidence_collapse":
        return "MISSING_EVIDENCE_COLLAPSE" in result_summary["drift_events"] and household(result_summary, "H-004")["disposition"] == "ASSIGNABLE", "existing unverified record could not silently become confirmed"
    return False, "unknown control"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("pipeline")
    parser.add_argument("output")
    args = parser.parse_args()
    input_path = Path(args.input).resolve()
    pipeline = Path(args.pipeline).resolve()
    package_root = pipeline.parent.parent
    controls_root = package_root / "controls"
    if controls_root.exists():
        shutil.rmtree(controls_root)
    controls_root.mkdir(parents=True)
    baseline_run = package_root / "executions" / "run_1"
    baseline_summary = output_summary(baseline_run)
    baseline_input = input_path
    names = [
        "confirmed_safety_to_unverified",
        "accessibility_need_removed",
        "capacity_reduced_below_demand",
        "duplicate_resource_reservation",
        "duplicate_household",
        "stale_record_newer_without_matching_authority",
        "unauthorized_priority_rule_added",
        "negative_control_memo_altered",
        "labels_permuted",
        "downstream_assignment_injection",
        "supporting_new_confirmation",
        "conclusory_assertion_only",
        "unsupported_confirmation",
        "priority_inversion",
        "missing_evidence_collapse",
        "intermediate_allocation_tamper",
    ]
    results = {}
    commands = []
    for name in names:
        case_dir = controls_root / name
        if case_dir.exists():
            shutil.rmtree(case_dir)
        case_dir.mkdir(parents=True)
        if name == "intermediate_allocation_tamper":
            tampered = case_dir / "tampered_allocationbridge.json"
            value = load_json(baseline_run / "allocationbridge.json")
            value["allocation_records"][0]["disposition"] = "REVIEW_REQUIRED"
            write_json(tampered, value)
            final_path = baseline_run / "final_chain.json"
            command = [sys.executable, str(pipeline.parent / "downstream_guard.py"), str(tampered), str(final_path)]
            process = subprocess.run(command, cwd=package_root, text=True, capture_output=True, check=False)
            (case_dir / "guard.stdout.txt").write_text(process.stdout, encoding="utf-8")
            (case_dir / "guard.stderr.txt").write_text(process.stderr, encoding="utf-8")
            commands.append(" ".join(command))
            passed = process.returncode != 0 and '"status": "REJECTED"' in process.stdout
            results[name] = {"status": "PASS" if passed else "FAIL", "execution": "tampered intermediate output", "assertion": "downstream hash guard rejects altered allocation output", "observed": process.stdout.strip(), "exit_code": process.returncode}
            continue
        mutated = mutate(load_json(input_path), name)
        mutated_path = case_dir / "input.json"
        write_json(mutated_path, mutated)
        process, output_dir, command = run_case(case_dir, mutated_path, pipeline, package_root, baseline_input, baseline_run)
        commands.append(" ".join(command))
        if process.returncode != 0:
            results[name] = {"status": "FAIL", "execution": "mutated input pipeline", "exit_code": process.returncode, "stderr": process.stderr}
            continue
        summary = output_summary(output_dir)
        rules = load_json(output_dir / "rulebinder.json")
        intake = load_json(output_dir / "intakebinder.json")
        capacity = load_json(output_dir / "capacityledger.json")
        final = load_json(output_dir / "final_chain.json")
        passed, assertion = assert_case(name, baseline_summary, summary, rules, intake, capacity, final)
        results[name] = {"status": "PASS" if passed else "FAIL", "execution": "mutated input pipeline", "input_sha256": file_sha256(mutated_path), "output_sha256": file_sha256(output_dir / "final_chain.json"), "assertion": assertion, "observed": summary}
    passed_count = sum(item.get("status") == "PASS" for item in results.values())
    report = {"schema": "shelterwise-control-results-v1", "canonical_input_sha256": file_sha256(input_path), "control_count": len(results), "actual_mutated_input_pipeline_executions": len(results) - 1, "actual_intermediate_tamper_executions": 1, "pass_count": passed_count, "fail_count": len(results) - passed_count, "controls": results, "commands": commands}
    write_json(args.output, report)
    print(json.dumps({"status": "PASS" if passed_count == len(results) else "FAIL", "pass_count": passed_count, "fail_count": len(results) - passed_count}, sort_keys=True))
    raise SystemExit(0 if passed_count == len(results) else 1)


if __name__ == "__main__":
    main()
