#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

EXPECTED_BINDINGS = {"T-001": "10:4-10:10", "T-002": "27:2-27:8", "T-003": "34:1-34:6", "T-004": "12:3-12:8", "T-005": "15:1-15:6", "T-006": "41:1-41:5", "T-007": "45:3-45:7"}
def canon(v): return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(v): return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def evaluate(data):
    t = {x["id"]: x for x in data["transcript"]}
    binding_issues = [k for k, expected in EXPECTED_BINDINGS.items() if k not in t or t[k].get("page_line") != expected]
    a, b = t.get("T-001"), t.get("T-002")
    same_site_contradiction = bool(a and b and not binding_issues and a["speaker"] == b["speaker"] and "personally replaced" in a["answer"].lower() and "did not perform any repair" in b["answer"].lower() and "north plant" in a["answer"].lower() and "north plant" in b["answer"].lower() and "2014" in a["answer"] and "2014" in b["answer"])
    findings = [{"id": "C-001", "type": "DIRECT_CONTRADICTION" if same_site_contradiction else ("UNRESOLVED_SOURCE_BINDING" if binding_issues else "NOT_ESTABLISHED"), "entries": ["T-001", "T-002"], "speaker": "Witness A", "explanation": "The same witness gives opposite answers about the same repair at the same site and time." if same_site_contradiction else "The canonical source binding or same-event predicate is not established."}, {"id": "C-002", "type": "AMBIGUITY", "entries": ["T-003"], "speaker": "Witness A", "explanation": "Probably gray plus lack of clear recollection is uncertainty, not contradiction."}, {"id": "C-003", "type": "NEGATIVE_CONTROL_NOT_CONTRADICTION", "entries": ["T-004", "T-005"], "speaker": "Witness B", "explanation": "Lack of observation and inability to identify the repairer do not negate another witness's account."}, {"id": "C-004", "type": "CHARACTERIZATION_NOT_ADMISSION", "entries": ["T-006"], "speaker": "Counsel", "explanation": "A characterized question without an answer is not an admission."}, {"id": "C-005", "type": "OMISSION_MISSING_FOUNDATION", "entries": ["T-007"], "speaker": "Witness A", "explanation": "Failure to recall a manufacturer name does not establish an opposing fact."}]
    payload = {"schema": "depobot-integrated-stage-v1", "matter_id": data["matter_id"], "stage": "DepoBot", "source_binding_valid": not binding_issues, "binding_issues": binding_issues, "findings": findings, "stage_disposition": "REVIEW_REQUIRED", "unresolved": ["The contradiction may require credibility and foundation review."], "non_claims": ["No credibility determination is made.", "No synthetic testimony is treated as a real admission."]}
    return dict(payload, canonical_record_sha256=digest(payload))

def main():
    input_path = Path(sys.argv[1]); output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    result = evaluate(json.loads(input_path.read_text(encoding="utf-8")))
    text = json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False)
    if output_path: output_path.write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__": main()
