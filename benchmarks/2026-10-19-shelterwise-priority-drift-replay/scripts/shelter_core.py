#!/usr/bin/env python3
"""Primary deterministic ShelterWise implementation.

The functions in this file deliberately operate on the supplied synthetic
record only.  No network, model, or real-world shelter data is consulted.
"""

from collections import defaultdict
from pathlib import Path

from common import changed_records, load_json, object_sha256, source_binding_errors, source_map


SPECIFICATION = load_json(Path(__file__).resolve().parent.parent / "specification.json")
KNOWN_RULE_IDS = set(SPECIFICATION["known_rule_ids"])
PRIORITY_BY_NEED = SPECIFICATION["priority_by_need_type"]


def _id(record):
    return record.get("record_id", record.get("resource_id", record.get("reservation_id", record.get("rule_id"))))


def bind_rules(data):
    sources = source_map(data)
    errors = []
    bound = []
    by_key = defaultdict(list)
    for rule in data.get("rules", []):
        errors.extend(source_binding_errors(rule, sources, {"rulebook"}, "rule"))
        source = sources.get(rule.get("source_id"), {})
        if source.get("priority_level") != rule.get("priority_level"):
            errors.append({"record_id": _id(rule), "kind": "RULE_PRIORITY_SOURCE_MISMATCH", "observed": rule.get("priority_level"), "source": source.get("priority_level")})
        if rule.get("rule_id") not in KNOWN_RULE_IDS:
            errors.append({"record_id": _id(rule), "kind": "UNAUTHORIZED_RULE_CHANGE", "reason": "rule identifier is outside the governing synthetic rule set"})
        key = (rule.get("authority_key"), rule.get("subject"), str(rule.get("applicable_period")))
        by_key[key].append(rule)
        bound.append({
            "rule_id": rule.get("rule_id"),
            "authority_key": rule.get("authority_key"),
            "subject": rule.get("subject"),
            "issued_at": rule.get("issued_at"),
            "effective_date": rule.get("effective_date"),
            "applicable_period": rule.get("applicable_period"),
            "priority_level": rule.get("priority_level"),
            "source_id": rule.get("source_id"),
            "source_location": rule.get("source_location"),
            "exact_source_fragment": rule.get("exact_source_fragment"),
            "text": rule.get("text"),
        })

    active = []
    superseded = []
    for key, candidates in sorted(by_key.items(), key=lambda item: str(item[0])):
        candidates = sorted(candidates, key=lambda item: (item.get("issued_at", ""), item.get("rule_id", "")))
        latest = candidates[-1]
        if len(candidates) > 1:
            for older in candidates[:-1]:
                if latest.get("authority_key") != older.get("authority_key") or latest.get("subject") != older.get("subject") or latest.get("applicable_period") != older.get("applicable_period"):
                    errors.append({"record_id": _id(latest), "kind": "UNAUTHORIZED_RULE_CHANGE", "reason": "newer record lacks the same authority, subject, and applicable period"})
                elif older.get("rule_id") not in latest.get("supersedes", [older.get("rule_id")]):
                    errors.append({"record_id": _id(latest), "kind": "UNAUTHORIZED_RULE_CHANGE", "reason": "newer same-key record does not disclose supersession"})
                else:
                    superseded.append({"older_rule_id": older.get("rule_id"), "by_rule_id": latest.get("rule_id")})
        if latest.get("rule_id") in KNOWN_RULE_IDS and not any(error.get("record_id") == _id(latest) and error.get("kind") in {"SOURCE_NOT_FOUND", "SOURCE_FRAGMENT_MISMATCH", "SOURCE_LOCATION_MISMATCH", "UNAUTHORIZED_SOURCE_TYPE", "RULE_PRIORITY_SOURCE_MISMATCH"} for error in errors):
            active.append(latest)

    active.sort(key=lambda item: (item.get("priority_level", 999), item.get("rule_id", "")))
    return {
        "schema": "shelterwise-rulebinder-output-v1",
        "bound_rule_count": len(bound),
        "bound_rules": sorted(bound, key=lambda item: item.get("rule_id", "")),
        "active_rule_ids": [item.get("rule_id") for item in active],
        "active_rules": active,
        "priority_order": [{"rule_id": item.get("rule_id"), "subject": item.get("subject"), "priority_level": item.get("priority_level")} for item in active],
        "superseded_rules": superseded,
        "errors": sorted(errors, key=lambda item: (str(item.get("record_id")), item.get("kind", ""))),
        "status": "PASS" if not errors else "REVIEW_REQUIRED",
    }


def _evidence_status(records, binding_errors):
    if not records:
        return "MISSING", [], []
    values = sorted({str(record.get("value")) for record in records})
    statuses = {record.get("status") for record in records}
    if any(error.get("record_id") in {_id(record) for record in records} and error.get("kind") in {"SOURCE_NOT_FOUND", "SOURCE_FRAGMENT_MISMATCH", "SOURCE_LOCATION_MISMATCH", "UNAUTHORIZED_SOURCE_TYPE", "MISSING_SOURCE_BINDING", "UNSUPPORTED_CONFIRMATION"} for error in binding_errors):
        return "UNVERIFIED", values, sorted(statuses)
    if "CONTRADICTED" in statuses or len(values) > 1:
        return "DISPUTED", values, sorted(statuses)
    if "CONFIRMED" in statuses:
        return "CONFIRMED", values, sorted(statuses)
    if "UNVERIFIED" in statuses:
        return "UNVERIFIED", values, sorted(statuses)
    return "MISSING", values, sorted(statuses)


def bind_intake(data, rules_output):
    sources = source_map(data)
    errors = []
    bound_records = []
    grouped = defaultdict(list)
    supported_confirmations = []
    for record in data.get("intake_records", []):
        record_errors = source_binding_errors(record, sources, {"intake", "supporting_intake"}, "intake")
        errors.extend(record_errors)
        source = sources.get(record.get("source_id"), {})
        if record.get("status") == "CONFIRMED" and "confirmed" not in str(record.get("exact_source_fragment", "")).lower():
            error = {"record_id": _id(record), "kind": "UNSUPPORTED_CONFIRMATION", "reason": "confirmed status is not supported by the preserved source fragment"}
            errors.append(error)
            record_errors.append(error)
        if record.get("status") == "CONFIRMED" and source.get("source_type") in {"intake", "supporting_intake"} and "confirmed" in str(record.get("exact_source_fragment", "")).lower() and not record_errors:
            supported_confirmations.append(_id(record))
        bound_records.append({
            "record_id": _id(record),
            "household_id": record.get("household_id"),
            "need_type": record.get("need_type"),
            "value": record.get("value"),
            "status": record.get("status"),
            "timestamp": record.get("timestamp"),
            "speaker_or_source": record.get("speaker_or_source"),
            "applicable_period": record.get("applicable_period"),
            "source_id": record.get("source_id"),
            "source_location": record.get("source_location"),
            "exact_source_fragment": record.get("exact_source_fragment"),
        })
        grouped[(record.get("household_id"), record.get("need_type"))].append(record)

    profile_by_id = {profile.get("household_id"): profile for profile in data.get("household_profiles", [])}
    needs_by_household = defaultdict(dict)
    for (household_id, need_type), records in sorted(grouped.items()):
        relevant_errors = [error for error in errors if error.get("record_id") in {_id(record) for record in records}]
        status, values, statuses = _evidence_status(records, relevant_errors)
        needs_by_household[household_id][need_type] = {
            "need_type": need_type,
            "status": status,
            "values": values,
            "record_ids": sorted(_id(record) for record in records),
            "observed_statuses": statuses,
        }

    duplicate_keys = defaultdict(list)
    for profile in data.get("household_profiles", []):
        duplicate_keys[profile.get("duplicate_key")].append(profile.get("household_id"))
    duplicate_candidates = [{"duplicate_key": key, "household_ids": sorted(ids)} for key, ids in sorted(duplicate_keys.items()) if key and len(ids) > 1]

    household_outputs = []
    rule_priorities = {item.get("subject"): item.get("priority_level") for item in rules_output.get("active_rules", [])}
    for profile in sorted(data.get("household_profiles", []), key=lambda item: item.get("household_id", "")):
        household_id = profile.get("household_id")
        profile_needs = needs_by_household.get(household_id, {})
        need_summaries = []
        for need in profile.get("needs", []):
            summary = dict(profile_needs.get(need.get("need_type"), {"need_type": need.get("need_type"), "status": "MISSING", "values": [], "record_ids": [], "observed_statuses": []}))
            summary.update({"required_resource": need.get("required_resource"), "quantity": need.get("quantity"), "accessible": bool(need.get("accessible"))})
            need_summaries.append(summary)
        priorities = []
        for need in need_summaries:
            if need["status"] == "CONFIRMED":
                subject = {"immediate_safety": "immediate safety priority", "accessibility": "accessibility accommodation", "family_unity": "family unity", "childcare": "child-care support"}.get(need.get("need_type"))
                priorities.append(rule_priorities.get(subject, PRIORITY_BY_NEED["other_confirmed"]))
            elif need["status"] == "DISPUTED":
                priorities.append(PRIORITY_BY_NEED["disputed"])
            elif need["status"] in {"UNVERIFIED", "MISSING"}:
                priorities.append(PRIORITY_BY_NEED["unverified_or_missing"])
            else:
                priorities.append(PRIORITY_BY_NEED["other_confirmed"])
        priority = min(priorities) if priorities else 7
        household_outputs.append({
            "household_id": household_id,
            "family_size": profile.get("family_size"),
            "priority_level": priority,
            "priority_basis": [need.get("need_type") for need in need_summaries if need.get("status") == "CONFIRMED"],
            "needs": sorted(need_summaries, key=lambda item: item.get("need_type", "")),
            "duplicate_key": profile.get("duplicate_key"),
        })

    return {
        "schema": "shelterwise-intakebinder-output-v1",
        "bound_record_count": len(bound_records),
        "bound_records": sorted(bound_records, key=lambda item: item.get("record_id", "")),
        "households": household_outputs,
        "duplicate_household_candidates": duplicate_candidates,
        "supported_confirmations": sorted(supported_confirmations),
        "errors": sorted(errors, key=lambda item: (str(item.get("record_id")), item.get("kind", ""))),
        "status": "PASS" if not errors else "REVIEW_REQUIRED",
    }


def ledger_capacity(data):
    sources = source_map(data)
    errors = []
    resources = {}
    for record in data.get("inventory", {}).get("resource_records", []):
        errors.extend(source_binding_errors(record, sources, {"inventory"}, "inventory"))
        resource_id = record.get("resource_id")
        if resource_id in resources:
            errors.append({"record_id": resource_id, "kind": "DUPLICATE_RESOURCE_RECORD"})
        resources[resource_id] = record
    reservations = []
    for record in data.get("inventory", {}).get("reservations", []):
        errors.extend(source_binding_errors(record, sources, {"reservation"}, "reservation"))
        reservations.append(record)
        if record.get("resource_id") not in resources:
            errors.append({"record_id": _id(record), "kind": "RESOURCE_NOT_FOUND", "resource_id": record.get("resource_id")})
        if record.get("quantity", 0) <= 0:
            errors.append({"record_id": _id(record), "kind": "INVALID_RESERVATION_QUANTITY"})

    by_resource = defaultdict(list)
    for reservation in reservations:
        if reservation.get("status") == "ACTIVE":
            by_resource[reservation.get("resource_id")].append(reservation)

    ledger = []
    duplicate_reservations = []
    over_allocations = []
    for resource_id, resource in sorted(resources.items()):
        active = by_resource.get(resource_id, [])
        reserved_quantity = sum(item.get("quantity", 0) for item in active)
        household_ids = sorted({item.get("household_id") for item in active})
        if resource.get("exclusive", resource.get("capacity", 0) == 1) and len(household_ids) > 1:
            duplicate_reservations.append({"resource_id": resource_id, "household_ids": household_ids, "reservation_ids": sorted(item.get("reservation_id") for item in active)})
        if reserved_quantity > resource.get("capacity", 0):
            over_allocations.append({"resource_id": resource_id, "capacity": resource.get("capacity"), "reserved_quantity": reserved_quantity})
        ledger.append({
            "resource_id": resource_id,
            "resource_type": resource.get("resource_type"),
            "capacity": resource.get("capacity"),
            "reserved_quantity": reserved_quantity,
            "available_capacity": resource.get("capacity", 0) - reserved_quantity,
            "accessible": bool(resource.get("accessible")),
            "exclusive": bool(resource.get("exclusive", resource.get("capacity", 0) == 1)),
            "status": resource.get("status"),
            "reserved_by": household_ids,
            "reservation_ids": sorted(item.get("reservation_id") for item in active),
        })

    unresolved = []
    unresolved.extend({"kind": "DUPLICATE_ASSIGNMENT", **item} for item in duplicate_reservations)
    unresolved.extend({"kind": "CAPACITY_OVER_ALLOCATION", **item} for item in over_allocations)
    unresolved.extend({"kind": error.get("kind"), "record_id": error.get("record_id")} for error in errors)
    return {
        "schema": "shelterwise-capacityledger-output-v1",
        "resource_count": len(resources),
        "reservation_count": len(reservations),
        "resource_ledger": ledger,
        "duplicate_reservations": duplicate_reservations,
        "over_allocations": over_allocations,
        "unresolved_capacity_conflicts": unresolved,
        "errors": sorted(errors, key=lambda item: (str(item.get("record_id")), item.get("kind", ""))),
        "status": "PASS" if not errors and not unresolved else "REVIEW_REQUIRED",
    }


def _resource_candidates(ledger, need):
    candidates = []
    for resource in ledger.get("resource_ledger", []):
        if resource.get("resource_type") != need.get("required_resource"):
            continue
        if need.get("accessible") and not resource.get("accessible"):
            continue
        candidates.append(resource)
    return candidates


def allocate(data, rules_output, intake_output, ledger_output):
    household_by_id = {item.get("household_id"): item for item in intake_output.get("households", [])}
    ledger_by_id = {item.get("resource_id"): item for item in ledger_output.get("resource_ledger", [])}
    allocations = []
    for profile in sorted(data.get("household_profiles", []), key=lambda item: item.get("household_id", "")):
        household_id = profile.get("household_id")
        evidence = household_by_id.get(household_id, {"priority_level": 6, "needs": []})
        evidence_by_type = {item.get("need_type"): item for item in evidence.get("needs", [])}
        need_results = []
        for need in profile.get("needs", []):
            need_evidence = evidence_by_type.get(need.get("need_type"), {"status": "MISSING", "record_ids": [], "values": []})
            status = need_evidence.get("status")
            candidates = _resource_candidates(ledger_output, need)
            reservations_for_household = []
            for resource in candidates:
                if household_id in resource.get("reserved_by", []):
                    reservations_for_household.append(resource)
            proposed = []
            conflicts = []
            missing_foundation = []
            reason = ""
            if status == "MISSING":
                assignment_status = "INSUFFICIENT_RECORD"
                missing_foundation.append(f"NO_EVIDENCE:{need.get('need_type')}")
                reason = "No intake record establishes the need."
            elif status == "UNVERIFIED":
                assignment_status = "REVIEW_REQUIRED"
                missing_foundation.append(f"UNVERIFIED:{need.get('need_type')}")
                reason = "The supplied record preserves an unverified need."
            elif status == "DISPUTED":
                assignment_status = "HOLD_FOR_HUMAN_DECISION"
                conflicts.append(f"CONTRADICTORY:{need.get('need_type')}")
                reason = "The supplied records conflict; ambiguity is not treated as confirmation."
            elif status == "CONFIRMED":
                for resource in reservations_for_household:
                    if len(resource.get("reserved_by", [])) > 1 or resource.get("available_capacity", 0) < 0:
                        conflicts.append(f"DUPLICATE_OR_OVERALLOCATED:{resource.get('resource_id')}")
                    else:
                        proposed.append(resource.get("resource_id"))
                already = len(proposed)
                remaining = max(0, need.get("quantity", 0) - already)
                open_candidates = [resource for resource in candidates if not resource.get("reserved_by") and resource.get("available_capacity", 0) >= 1]
                for resource in open_candidates[:remaining]:
                    proposed.append(resource.get("resource_id"))
                if conflicts:
                    assignment_status = "REVIEW_REQUIRED"
                    reason = "A required resource is reserved for more than one household or is over capacity."
                elif len(proposed) >= need.get("quantity", 0):
                    assignment_status = "ASSIGNABLE"
                    reason = "Confirmed need and feasible, uniquely reserved or available resources are present."
                else:
                    assignment_status = "NO_FEASIBLE_ASSIGNMENT"
                    reason = "The confirmed need exceeds the feasible resource capacity in the ledger."
            else:
                assignment_status = "INSUFFICIENT_RECORD"
                missing_foundation.append(f"UNKNOWN_EVIDENCE_STATUS:{status}")
                reason = "The evidence status is not a disclosed state."
            need_results.append({
                "need_id": need.get("need_id"),
                "need_type": need.get("need_type"),
                "required_resource": need.get("required_resource"),
                "quantity": need.get("quantity"),
                "accessible": bool(need.get("accessible")),
                "evidence_status": status,
                "evidence_record_ids": sorted(need_evidence.get("record_ids", [])),
                "controlling_rule": {"need_type": need.get("need_type"), "priority_level": evidence.get("priority_level")},
                "proposed_resources": sorted(proposed),
                "supporting_evidence": sorted(need_evidence.get("record_ids", [])),
                "unmet_need": max(0, need.get("quantity", 0) - len(proposed)),
                "conflicts": sorted(conflicts),
                "missing_foundation": sorted(missing_foundation),
                "status": assignment_status,
                "reason": reason,
            })
        statuses = [item.get("status") for item in need_results]
        if "INSUFFICIENT_RECORD" in statuses:
            household_status = "INSUFFICIENT_RECORD"
        elif "HOLD_FOR_HUMAN_DECISION" in statuses:
            household_status = "HOLD_FOR_HUMAN_DECISION"
        elif "REVIEW_REQUIRED" in statuses:
            household_status = "REVIEW_REQUIRED"
        elif "NO_FEASIBLE_ASSIGNMENT" in statuses:
            household_status = "NO_FEASIBLE_ASSIGNMENT"
        else:
            household_status = "ASSIGNABLE"
        allocations.append({
            "household_id": household_id,
            "priority_level": evidence.get("priority_level"),
            "assignments": need_results,
            "disposition": household_status,
        })

    status_counts = defaultdict(int)
    for allocation in allocations:
        status_counts[allocation.get("disposition")] += 1
    return {
        "schema": "shelterwise-allocationbridge-output-v1",
        "allocation_records": allocations,
        "status_counts": dict(sorted(status_counts.items())),
        "negative_control_used": False,
        "boundaries": [
            "household identity != priority",
            "need allegation != confirmed need",
            "resource reservation != unique assignment",
            "capacity != feasibility when evidence is missing",
            "unverified information != disproved information",
        ],
        "status": "PASS" if not any(item.get("disposition") == "INSUFFICIENT_RECORD" for item in allocations) else "REVIEW_REQUIRED",
    }


def drift_shield(data, baseline_data, rules_output, intake_output, ledger_output, allocation_output, baseline_final):
    events = []
    changes = changed_records(baseline_data, data)
    if any(error.get("kind") == "UNAUTHORIZED_RULE_CHANGE" for error in rules_output.get("errors", [])):
        events.append("UNAUTHORIZED_RULE_CHANGE")
    if any(error.get("kind") == "RULE_PRIORITY_SOURCE_MISMATCH" for error in rules_output.get("errors", [])):
        events.append("PRIORITY_INVERSION")
    if ledger_output.get("duplicate_reservations"):
        events.extend(["DUPLICATE_ASSIGNMENT", "CAPACITY_OVER_ALLOCATION"])
    if ledger_output.get("over_allocations"):
        events.append("CAPACITY_OVER_ALLOCATION")
    if any(error.get("kind") == "UNSUPPORTED_CONFIRMATION" for error in intake_output.get("errors", [])):
        events.append("UNSUPPORTED_CONFIRMATION")
    baseline_households = {item.get("household_id"): item for item in baseline_final.get("household_dispositions", [])}
    current_households = {item.get("household_id"): item for item in allocation_output.get("allocation_records", [])}
    for household_id, baseline_item in baseline_households.items():
        current_item = current_households.get(household_id, {})
        before_status = baseline_item.get("disposition")
        after_status = current_item.get("disposition")
        if before_status != after_status:
            continue
        before_priority = baseline_item.get("priority_level")
        after_priority = current_item.get("priority_level")
        if before_priority is not None and after_priority is not None and after_priority < before_priority:
            events.append("PRIORITY_INVERSION")
    baseline_intake = {item.get("household_id"): {need.get("need_type"): need for need in item.get("needs", [])} for item in baseline_final.get("intake_summary", [])}
    current_intake = {item.get("household_id"): {need.get("need_type"): need for need in item.get("needs", [])} for item in intake_output.get("households", [])}
    supported_change_ids = set(intake_output.get("supported_confirmations", []))
    baseline_intake_record_ids = {record_id for record in baseline_final.get("intake_summary", []) for need in record.get("needs", []) for record_id in need.get("record_ids", [])}
    for household_id, needs in baseline_intake.items():
        for need_type, baseline_need in needs.items():
            current_need = current_intake.get(household_id, {}).get(need_type, {})
            if baseline_need.get("status") in {"UNVERIFIED", "MISSING"} and current_need.get("status") == "CONFIRMED":
                records = set(current_need.get("record_ids", []))
                if records.intersection(supported_change_ids) and records.intersection(baseline_intake_record_ids):
                    events.append("MISSING_EVIDENCE_COLLAPSE")
                elif not records.intersection(supported_change_ids):
                    events.append("MISSING_EVIDENCE_COLLAPSE")
    if data.get("injected_assignments"):
        events.append("DOWNSTREAM_ASSIGNMENT_INJECTION")

    current_final_dispositions = [{"household_id": item.get("household_id"), "priority_level": item.get("priority_level"), "disposition": item.get("disposition")} for item in allocation_output.get("allocation_records", [])]
    baseline_dispositions = baseline_final.get("household_dispositions", [])
    changed_outcomes = current_final_dispositions != baseline_dispositions
    if changed_outcomes and not changes:
        events.append("DOWNSTREAM_ASSIGNMENT_INJECTION")

    return {
        "schema": "shelterwise-driftshield-output-v1",
        "changed_records": changes,
        "events": sorted(set(events)),
        "changed_outcomes": changed_outcomes,
        "baseline_disposition": baseline_final.get("disposition"),
        "current_household_dispositions": current_final_dispositions,
        "baseline_household_dispositions": baseline_dispositions,
        "status": "DRIFT_DETECTED" if events or changed_outcomes else "NO_DRIFT",
    }


def final_chain(data, rules_output, intake_output, ledger_output, allocation_output, drift_output):
    blocking_errors = bool(rules_output.get("errors") or intake_output.get("errors") or ledger_output.get("errors"))
    unresolved = []
    unresolved.extend({"stage": "RuleBinder", "kind": error.get("kind"), "record_id": error.get("record_id")} for error in rules_output.get("errors", []))
    unresolved.extend({"stage": "IntakeBinder", "kind": error.get("kind"), "record_id": error.get("record_id")} for error in intake_output.get("errors", []))
    unresolved.extend({"stage": "CapacityLedger", "kind": error.get("kind"), "record_id": error.get("record_id")} for error in ledger_output.get("errors", []))
    unresolved.extend({"stage": "CapacityLedger", "kind": item.get("kind"), "resource_id": item.get("resource_id")} for item in ledger_output.get("unresolved_capacity_conflicts", []))
    for allocation in allocation_output.get("allocation_records", []):
        if allocation.get("disposition") != "ASSIGNABLE":
            unresolved.append({"stage": "AllocationBridge", "household_id": allocation.get("household_id"), "disposition": allocation.get("disposition")})
    unresolved.extend({"stage": "DriftShield", "event": event} for event in drift_output.get("events", []))
    if blocking_errors:
        disposition = "INSUFFICIENT_RECORD"
    elif unresolved:
        disposition = "REVIEW_REQUIRED"
    else:
        disposition = "ASSIGNABLE"
    stage_hashes = {
        "rulebinder": object_sha256(rules_output),
        "intakebinder": object_sha256(intake_output),
        "capacityledger": object_sha256(ledger_output),
        "allocationbridge": object_sha256(allocation_output),
        "driftshield": object_sha256(drift_output),
    }
    return {
        "schema": "shelterwise-final-chain-output-v1",
        "matter_id": data.get("matter", {}).get("matter_id"),
        "synthetic_fixture": data.get("matter", {}).get("synthetic_fixture"),
        "baseline_question": data.get("matter", {}).get("baseline_question"),
        "disposition": disposition,
        "cleanest_record_basis": "The synthetic record preserves rule bindings, intake uncertainty, resource conflicts, and assignment-level dispositions; unresolved conflicts prevent an all-assignable result.",
        "household_dispositions": [{"household_id": item.get("household_id"), "priority_level": item.get("priority_level"), "disposition": item.get("disposition")} for item in allocation_output.get("allocation_records", [])],
        "intake_summary": intake_output.get("households", []),
        "resource_conflicts": ledger_output.get("unresolved_capacity_conflicts", []),
        "unresolved_items": unresolved,
        "drift_events": drift_output.get("events", []),
        "boundaries": allocation_output.get("boundaries", []),
        "stage_hashes": stage_hashes,
        "measured_results_are_not_real_world_advice": True,
    }
