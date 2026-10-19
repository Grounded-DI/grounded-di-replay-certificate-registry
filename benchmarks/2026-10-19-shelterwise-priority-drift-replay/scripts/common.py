#!/usr/bin/env python3
"""Small deterministic helpers shared by the primary ShelterWise stages."""

import hashlib
import json
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def object_sha256(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_map(data):
    return {source["source_id"]: source for source in data.get("sources", [])}


def source_binding_errors(record, sources, expected_types, kind):
    errors = []
    required = ["source_id", "source_location", "exact_source_fragment"]
    missing = [field for field in required if not record.get(field)]
    if missing:
        errors.append({"record_id": record.get("record_id", record.get("resource_id", record.get("reservation_id", record.get("rule_id")))), "kind": "MISSING_SOURCE_BINDING", "fields": missing, "record_kind": kind})
        return errors
    source = sources.get(record["source_id"])
    if source is None:
        errors.append({"record_id": record.get("record_id", record.get("resource_id", record.get("reservation_id", record.get("rule_id")))), "kind": "SOURCE_NOT_FOUND", "source_id": record["source_id"], "record_kind": kind})
        return errors
    if source.get("source_location") != record.get("source_location"):
        errors.append({"record_id": record.get("record_id", record.get("resource_id", record.get("reservation_id", record.get("rule_id")))), "kind": "SOURCE_LOCATION_MISMATCH", "source_id": record["source_id"], "record_kind": kind})
    if source.get("exact_source_fragment") != record.get("exact_source_fragment"):
        errors.append({"record_id": record.get("record_id", record.get("resource_id", record.get("reservation_id", record.get("rule_id")))), "kind": "SOURCE_FRAGMENT_MISMATCH", "source_id": record["source_id"], "record_kind": kind})
    if expected_types and source.get("source_type") not in expected_types:
        errors.append({"record_id": record.get("record_id", record.get("resource_id", record.get("reservation_id", record.get("rule_id")))), "kind": "UNAUTHORIZED_SOURCE_TYPE", "source_id": record["source_id"], "observed": source.get("source_type"), "allowed": sorted(expected_types), "record_kind": kind})
    return errors


def record_identity_map(data):
    collections = {
        "rules": ("rule_id", data.get("rules", [])),
        "intake_records": ("record_id", data.get("intake_records", [])),
        "resource_records": ("resource_id", data.get("inventory", {}).get("resource_records", [])),
        "reservations": ("reservation_id", data.get("inventory", {}).get("reservations", [])),
        "household_profiles": ("household_id", data.get("household_profiles", [])),
        "negative_control_memos": ("memo_id", data.get("negative_control_memos", [])),
    }
    result = {}
    for collection, (key, records) in collections.items():
        for record in records:
            result[f"{collection}:{record.get(key)}"] = object_sha256(record)
    result["top_level:injected_assignments"] = object_sha256(data.get("injected_assignments", []))
    return result


def changed_records(baseline_data, current_data):
    before = record_identity_map(baseline_data)
    after = record_identity_map(current_data)
    changes = []
    for key in sorted(set(before) | set(after)):
        if key not in before:
            changes.append({"record": key, "change": "ADDED"})
        elif key not in after:
            changes.append({"record": key, "change": "REMOVED"})
        elif before[key] != after[key]:
            changes.append({"record": key, "change": "ALTERED"})
    return changes
