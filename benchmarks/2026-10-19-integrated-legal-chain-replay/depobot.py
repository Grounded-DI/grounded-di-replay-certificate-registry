#!/usr/bin/env python3
"""Synthetic DepoBot stage: source-linked testimony matrix."""
import hashlib
import json
import sys
from pathlib import Path

EXPECTED_BINDINGS = {
    "T-001": "10:4-10:10",
    "T-002": "27:2-27:8",
    "T-003": "34:1-34:6",
    "T-004": "12:3-12:8",
    "T-005": "15:1-15:6",
    "T-006": "41:1-41:5",
    "T-007": "45:3-45:7",
}


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_payload(payload):
    return hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest()


def evaluate(data):
    transcript = {item["id"]: item for item in data["transcript"]}
    binding_issues = []
    for entry_id, expected_page_line in EXPECTED_BINDINGS.items():
        entry = transcript.get(entry_id)
        if entry is None:
            binding_issues.append({"entry_id": entry_id, "reason": "missing_entry", "expected_page_line": expected_page_line})
        elif entry.get("page_line") != expected_page_line:
            binding_issues.append({
                "entry_id": entry_id,
                "reason": "page_line_mismatch",
                "expected_page_line": expected_page_line,
                "observed_page_line": entry.get("page_line"),
            })
    testimony_matrix = []
    for entry in data["transcript"]:
        testimony_matrix.append({
            "id": entry["id"],
            "speaker": entry["speaker"],
            "question": entry["question"],
            "answer": entry["answer"],
            "page_line": entry["page_line"],
            "exhibit": entry["exhibit"],
            "source_fragment": entry["source_fragment"],
            "kind": entry["kind"],
        })
    first = transcript.get("T-001")
    second = transcript.get("T-002")
    contradiction = bool(
        not binding_issues
        and first and second
        and first.get("speaker") == second.get("speaker") == "Witness A"
        and "personally replaced" in first.get("answer", "").lower()
        and "did not perform any repair" in second.get("answer", "").lower()
        and "north plant" in first.get("answer", "").lower()
        and "north plant" in second.get("answer", "").lower()
        and "2014" in first.get("answer", "")
        and "2014" in second.get("answer", "")
    )
    findings = [
        {
            "id": "C-001",
            "type": "DIRECT_CONTRADICTION" if contradiction else ("UNRESOLVED_SOURCE_BINDING" if binding_issues else "NOT_ESTABLISHED"),
            "entries": ["T-001", "T-002"],
            "speaker": "Witness A",
            "explanation": (
                "The same witness gives opposite answers about the same repair at the same site and time."
                if contradiction else
                "The canonical source binding or same-event predicate is not established."
            ),
        },
        {
            "id": "C-002",
            "type": "AMBIGUITY",
            "entries": ["T-003"],
            "speaker": "Witness A",
            "explanation": "Probably gray plus lack of clear recollection is uncertainty, not contradiction.",
        },
        {
            "id": "C-003",
            "type": "NEGATIVE_CONTROL_NOT_CONTRADICTION",
            "entries": ["T-004", "T-005"],
            "speaker": "Witness B",
            "explanation": "Lack of observation and inability to identify the repairer do not negate another witness's account.",
        },
        {
            "id": "C-004",
            "type": "CHARACTERIZATION_NOT_ADMISSION",
            "entries": ["T-006"],
            "speaker": "Counsel",
            "explanation": "A characterized question without an answer is not an admission.",
        },
        {
            "id": "C-005",
            "type": "OMISSION_MISSING_FOUNDATION",
            "entries": ["T-007"],
            "speaker": "Witness A",
            "explanation": "Failure to recall a manufacturer name does not establish an opposing fact.",
        },
    ]
    payload = {
        "schema": "depobot-integrated-stage-v2",
        "matter_id": data["matter_id"],
        "stage": "DepoBot",
        "synthetic_fixture": True,
        "source_binding_valid": not binding_issues,
        "binding_issues": binding_issues,
        "testimony_matrix": testimony_matrix,
        "findings": findings,
        "stage_disposition": "REVIEW_REQUIRED",
        "unresolved": ["The contradiction may require credibility and foundation review."],
        "non_claims": [
            "No credibility determination is made.",
            "No synthetic testimony is treated as a real admission.",
        ],
    }
    return dict(payload, canonical_record_sha256=sha256_payload(payload))


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: depobot.py INPUT.json [OUTPUT.json]")
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    result = evaluate(json.loads(input_path.read_text(encoding="utf-8")))
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    if output_path:
        output_path.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
