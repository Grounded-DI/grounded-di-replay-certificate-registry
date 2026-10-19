#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def canon(v): return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(v): return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def main(input_path=None):
    data = json.loads((Path(input_path) if input_path else ROOT / "input.json").read_text(encoding="utf-8"))
    t = {x["id"]: x for x in data["transcript"]}
    same_site_contradiction = ("personally installed" in t["T-001"]["answer"].lower() and "did not perform any installation work" in t["T-002"]["answer"].lower() and "north plant" in t["T-001"]["answer"].lower() and "north plant" in t["T-002"]["answer"].lower())
    findings = [
        {"id": "C-001", "type": "DIRECT_CONTRADICTION" if same_site_contradiction else "NOT_ESTABLISHED", "entries": ["T-001", "T-002"], "speaker": "Witness A", "explanation": "The same witness affirmatively states both that he personally installed the pump and that he performed no installation work at the same site." if same_site_contradiction else "The altered answers no longer establish the same-site contradiction under the disclosed rule."},
        {"id": "C-002", "type": "AMBIGUITY", "entries": ["T-003"], "speaker": "Witness A", "explanation": "Probably blue plus an express lack of clear recollection is uncertainty, not a contradiction."},
        {"id": "C-003", "type": "OMISSION_MISSING_FOUNDATION", "entries": ["T-004"], "speaker": "Witness A", "explanation": "Failure to recall a manufacturer nameplate does not establish an opposing fact."},
        {"id": "C-004", "type": "NEGATIVE_CONTROL_NOT_CONTRADICTION", "entries": ["T-001", "T-005", "T-006"], "speaker": "Witness A / Witness B", "explanation": "Witness B's lack of observation and inability to identify the installer do not negate Witness A's account."},
        {"id": "C-005", "type": "CHARACTERIZATION_NOT_ADMISSION", "entries": ["T-007"], "speaker": "Counsel", "explanation": "The question contains a characterization, but there is no answer establishing an admission."},
    ]
    payload = {"schema": "depobot-testimony-contradiction-replay-v1", "matter_id": data["matter_id"], "closed_world": True, "findings": findings, "disposition": "REVIEW_REQUIRED", "unresolved_items": ["Whether either account can be reconciled through additional foundation or site records."], "non_claims": ["No credibility determination is made.", "No real testimony or legal admission is represented."]}
    print(json.dumps(dict(payload, canonical_record_sha256=digest(payload)), sort_keys=True, indent=2, ensure_ascii=False))

if __name__ == "__main__": main(sys.argv[1] if len(sys.argv) > 1 else None)
