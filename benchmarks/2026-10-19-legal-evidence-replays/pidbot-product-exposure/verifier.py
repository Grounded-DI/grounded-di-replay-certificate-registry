#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def canon(v): return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
def digest(v): return hashlib.sha256(canon(v).encode("utf-8")).hexdigest()

def main():
    expected = json.loads((ROOT / "expected_output.json").read_text())
    rows = {x["dimension"]: x for x in expected["evidence_matrix"]}
    checks = {
        "product_match_is_bounded": rows["product_identification"]["status"] == "MATCH",
        "component_separate": rows["component_identification"]["status"] == "REVIEW",
        "material_not_inferred": rows["material_content"]["status"] == "UNCERTAIN",
        "exposure_not_inferred": rows["exposure"]["status"] == "REVIEW",
        "dose_not_inferred": rows["dose"]["status"] == "UNCERTAIN",
        "causation_not_inferred": rows["causation"]["status"] == "UNCERTAIN",
        "liability_not_inferred": rows["legal_liability"]["status"] == "REVIEW",
        "separation_count": len(expected["separation_preserved"]) == 7,
        "hash_matches": expected["canonical_record_sha256"] == digest({k:v for k,v in expected.items() if k != "canonical_record_sha256"}),
    }
    result = {"verifier": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "scope": "closed-world synthetic fixture"}
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if result["verifier"] == "PASS" else 1)

if __name__ == "__main__": main()
