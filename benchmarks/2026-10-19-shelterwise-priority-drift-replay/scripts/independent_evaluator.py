#!/usr/bin/env python3
"""Independent source-record recalculation for the ShelterWise package.

This evaluator intentionally does not import shelter_core or any primary stage
module.  It recalculates the observed rule, intake, capacity, and allocation
fields directly from the canonical synthetic record.
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path

from common import file_sha256, load_json


def source_map(data):
    return {item.get("source_id"): item for item in data.get("sources", [])}


def identifier(record):
    return record.get("record_id", record.get("resource_id", record.get("reservation_id", record.get("rule_id"))))


def binding_ok(record, sources, allowed):
    source = sources.get(record.get("source_id"))
    return bool(source and source.get("source_location") == record.get("source_location") and source.get("exact_source_fragment") == record.get("exact_source_fragment") and source.get("source_type") in allowed)


def recalc_rules(data, specification):
    sources = source_map(data)
    known_rule_ids = set(specification["known_rule_ids"])
    active = []
    errors = []
    for rule in data.get("rules", []):
        source = sources.get(rule.get("source_id"), {})
        if not binding_ok(rule, sources, {"rulebook"}):
            errors.append(identifier(rule))
        if source.get("priority_level") != rule.get("priority_level"):
            errors.append(identifier(rule))
        if rule.get("rule_id") not in known_rule_ids:
            errors.append(identifier(rule))
        if rule.get("rule_id") in known_rule_ids and binding_ok(rule, sources, {"rulebook"}) and source.get("priority_level") == rule.get("priority_level"):
            active.append(rule)
    active.sort(key=lambda item: (item.get("priority_level", 999), item.get("rule_id", "")))
    return [item.get("rule_id") for item in active], sorted(set(errors))


def recalc_intake(data, specification):
    sources = source_map(data)
    grouped = defaultdict(list)
    errors = []
    for record in data.get("intake_records", []):
        source = sources.get(record.get("source_id"), {})
        valid = binding_ok(record, sources, {"intake", "supporting_intake"})
        if not valid:
            errors.append(identifier(record))
        if record.get("status") == "CONFIRMED" and "confirmed" not in str(record.get("exact_source_fragment", "")).lower():
            errors.append(identifier(record))
        grouped[(record.get("household_id"), record.get("need_type"))].append((record, valid))
    status_by_key = {}
    supported = set()
    for key, records in grouped.items():
        values = {str(record.get("value")) for record, _ in records}
        statuses = {record.get("status") for record, valid in records}
        valid_records = all(valid for _, valid in records)
        if not valid_records:
            status = "UNVERIFIED"
        elif "CONTRADICTED" in statuses or len(values) > 1:
            status = "DISPUTED"
        elif "CONFIRMED" in statuses:
            status = "CONFIRMED"
        elif "UNVERIFIED" in statuses:
            status = "UNVERIFIED"
        else:
            status = "MISSING"
        status_by_key[key] = status
        for record, valid in records:
            if valid and record.get("status") == "CONFIRMED":
                supported.add(identifier(record))
    rule_priority = {"immediate_safety": specification["priority_by_need_type"]["immediate_safety"], "accessibility": specification["priority_by_need_type"]["accessibility"], "family_unity": specification["priority_by_need_type"]["family_unity"], "childcare": specification["priority_by_need_type"]["childcare"]}
    households = []
    for profile in sorted(data.get("household_profiles", []), key=lambda item: item.get("household_id", "")):
        needs = []
        priority_values = []
        for need in profile.get("needs", []):
            status = status_by_key.get((profile.get("household_id"), need.get("need_type")), "MISSING")
            needs.append({"need_type": need.get("need_type"), "status": status, "record_ids": sorted(identifier(record) for record in data.get("intake_records", []) if record.get("household_id") == profile.get("household_id") and record.get("need_type") == need.get("need_type"))})
            if status == "CONFIRMED":
                priority_values.append(rule_priority.get(need.get("need_type"), specification["priority_by_need_type"]["other_confirmed"]))
            elif status == "DISPUTED":
                priority_values.append(specification["priority_by_need_type"]["disputed"])
            else:
                priority_values.append(specification["priority_by_need_type"]["unverified_or_missing"])
        households.append({"household_id": profile.get("household_id"), "priority_level": min(priority_values) if priority_values else 7, "needs": sorted(needs, key=lambda item: item.get("need_type", ""))})
    return households, errors, sorted(supported)


def recalc_capacity(data):
    sources = source_map(data)
    resources = {}
    errors = []
    for resource in data.get("inventory", {}).get("resource_records", []):
        if not binding_ok(resource, sources, {"inventory"}):
            errors.append(identifier(resource))
        resources[resource.get("resource_id")] = resource
    reservations = defaultdict(list)
    for reservation in data.get("inventory", {}).get("reservations", []):
        if not binding_ok(reservation, sources, {"reservation"}):
            errors.append(identifier(reservation))
        if reservation.get("status") == "ACTIVE":
            reservations[reservation.get("resource_id")].append(reservation)
    ledger = []
    duplicates = []
    for resource_id, resource in sorted(resources.items()):
        active = reservations.get(resource_id, [])
        reserved = sum(item.get("quantity", 0) for item in active)
        households = sorted({item.get("household_id") for item in active})
        if resource.get("exclusive", resource.get("capacity", 0) == 1) and len(households) > 1:
            duplicates.append(resource_id)
        ledger.append({"resource_id": resource_id, "resource_type": resource.get("resource_type"), "capacity": resource.get("capacity"), "reserved_quantity": reserved, "available_capacity": resource.get("capacity", 0) - reserved, "accessible": bool(resource.get("accessible")), "exclusive": bool(resource.get("exclusive", resource.get("capacity", 0) == 1)), "reserved_by": households})
    return ledger, sorted(duplicates), errors


def recalc_allocations(data, intake_households, ledger):
    intake_by_id = {item.get("household_id"): item for item in intake_households}
    ledger_by_id = {item.get("resource_id"): item for item in ledger}
    output = []
    for profile in sorted(data.get("household_profiles", []), key=lambda item: item.get("household_id", "")):
        household_id = profile.get("household_id")
        intake = intake_by_id[household_id]
        needs_by_type = {item.get("need_type"): item for item in intake.get("needs", [])}
        statuses = []
        for need in profile.get("needs", []):
            evidence = needs_by_type.get(need.get("need_type"), {"status": "MISSING", "record_ids": []})
            status = evidence.get("status")
            candidates = [item for item in ledger if item.get("resource_type") == need.get("required_resource") and (not need.get("accessible") or item.get("accessible"))]
            reserved = [item for item in candidates if household_id in item.get("reserved_by", [])]
            proposed = [item for item in reserved if len(item.get("reserved_by", [])) == 1 and item.get("available_capacity", 0) >= 0]
            conflicts = [item for item in reserved if len(item.get("reserved_by", [])) > 1 or item.get("available_capacity", 0) < 0]
            open_candidates = [item for item in candidates if not item.get("reserved_by") and item.get("available_capacity", 0) >= 1]
            if status == "MISSING":
                result = "INSUFFICIENT_RECORD"
            elif status == "UNVERIFIED":
                result = "REVIEW_REQUIRED"
            elif status == "DISPUTED":
                result = "HOLD_FOR_HUMAN_DECISION"
            elif status == "CONFIRMED":
                proposed_count = len(proposed) + min(len(open_candidates), max(0, need.get("quantity", 0) - len(proposed)))
                if conflicts:
                    result = "REVIEW_REQUIRED"
                elif proposed_count >= need.get("quantity", 0):
                    result = "ASSIGNABLE"
                else:
                    result = "NO_FEASIBLE_ASSIGNMENT"
            else:
                result = "INSUFFICIENT_RECORD"
            statuses.append(result)
        if "INSUFFICIENT_RECORD" in statuses:
            disposition = "INSUFFICIENT_RECORD"
        elif "HOLD_FOR_HUMAN_DECISION" in statuses:
            disposition = "HOLD_FOR_HUMAN_DECISION"
        elif "REVIEW_REQUIRED" in statuses:
            disposition = "REVIEW_REQUIRED"
        elif "NO_FEASIBLE_ASSIGNMENT" in statuses:
            disposition = "NO_FEASIBLE_ASSIGNMENT"
        else:
            disposition = "ASSIGNABLE"
        output.append({"household_id": household_id, "priority_level": intake.get("priority_level"), "disposition": disposition})
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("run_dir")
    args = parser.parse_args()
    data = load_json(args.input)
    run = Path(args.run_dir)
    specification = load_json(Path(args.input).parent / "specification.json")
    active_rules, rule_errors = recalc_rules(data, specification)
    intake_households, intake_errors, supported = recalc_intake(data, specification)
    ledger, duplicate_resources, capacity_errors = recalc_capacity(data)
    allocations = recalc_allocations(data, intake_households, ledger)
    final = load_json(run / "final_chain.json")
    observed_rules = load_json(run / "rulebinder.json")
    observed_intake = load_json(run / "intakebinder.json")
    observed_capacity = load_json(run / "capacityledger.json")
    observed_allocation = load_json(run / "allocationbridge.json")
    expected_final_disposition = "INSUFFICIENT_RECORD" if rule_errors or intake_errors or capacity_errors else ("REVIEW_REQUIRED" if any(item.get("disposition") != "ASSIGNABLE" for item in allocations) or duplicate_resources else "ASSIGNABLE")
    comparisons = {
        "rule_active_ids": observed_rules.get("active_rule_ids") == active_rules,
        "rule_error_count": len(observed_rules.get("errors", [])) == len(set(rule_errors)),
        "intake_households": [{"household_id": item.get("household_id"), "priority_level": item.get("priority_level"), "needs": [{"need_type": need.get("need_type"), "status": need.get("status"), "record_ids": need.get("record_ids")} for need in item.get("needs", [])]} for item in observed_intake.get("households", [])] == intake_households,
        "intake_supported_confirmations": observed_intake.get("supported_confirmations") == supported,
        "capacity_ledger": [{"resource_id": item.get("resource_id"), "resource_type": item.get("resource_type"), "capacity": item.get("capacity"), "reserved_quantity": item.get("reserved_quantity"), "available_capacity": item.get("available_capacity"), "accessible": item.get("accessible"), "exclusive": item.get("exclusive"), "reserved_by": item.get("reserved_by")} for item in observed_capacity.get("resource_ledger", [])] == ledger,
        "capacity_duplicates": [item.get("resource_id") for item in observed_capacity.get("duplicate_reservations", [])] == duplicate_resources,
        "capacity_error_count": len(observed_capacity.get("errors", [])) == len(capacity_errors),
        "allocations": [{"household_id": item.get("household_id"), "priority_level": item.get("priority_level"), "disposition": item.get("disposition")} for item in observed_allocation.get("allocation_records", [])] == allocations,
        "final_disposition": final.get("disposition") == expected_final_disposition,
    }
    passed = all(comparisons.values())
    result = {
        "schema": "shelterwise-independent-evaluator-v1",
        "status": "PASS" if passed else "FAIL",
        "imports_primary_stage_logic": False,
        "recalculation_source": "canonical synthetic source records",
        "calculated": {"active_rule_ids": active_rules, "rule_errors": sorted(set(rule_errors)), "intake_households": intake_households, "supported_confirmations": supported, "capacity_ledger": ledger, "duplicate_resources": duplicate_resources, "capacity_errors": sorted(capacity_errors), "allocations": allocations, "expected_final_disposition": expected_final_disposition},
        "comparisons": comparisons,
        "input_sha256": file_sha256(args.input),
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
