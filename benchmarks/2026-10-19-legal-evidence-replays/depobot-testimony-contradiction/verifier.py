#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
def canon(v): return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(v): return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def main():
    expected = json.loads((ROOT / "expected_output.json").read_text())
    kinds = {x["id"]: x["type"] for x in expected["findings"]}
    checks = {
        "one_direct_contradiction": kinds.get("C-001") == "DIRECT_CONTRADICTION",
        "ambiguity_not_contradiction": kinds.get("C-002") == "AMBIGUITY",
        "omission_preserved": kinds.get("C-003") == "OMISSION_MISSING_FOUNDATION",
        "negative_control_preserved": kinds.get("C-004") == "NEGATIVE_CONTROL_NOT_CONTRADICTION",
        "characterization_not_admission": kinds.get("C-005") == "CHARACTERIZATION_NOT_ADMISSION",
        "hash_matches": expected["canonical_record_sha256"] == digest({k:v for k,v in expected.items() if k != "canonical_record_sha256"}),
        "review_required": expected["disposition"] == "REVIEW_REQUIRED",
    }
    result = {"verifier": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "scope": "closed-world synthetic fixture"}
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if result["verifier"] == "PASS" else 1)

if __name__ == "__main__": main()
