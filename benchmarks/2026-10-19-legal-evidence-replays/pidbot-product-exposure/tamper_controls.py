#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def run(d):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "input.json"; p.write_text(json.dumps(d))
        r = subprocess.run([sys.executable, str(ROOT / "replay.py"), str(p)], capture_output=True, text=True, check=True)
        return json.loads(r.stdout)

def main():
    original = json.loads((ROOT / "input.json").read_text())
    altered = json.loads(json.dumps(original))
    altered["records"][1]["product_id"] = "MODEL-UNKNOWN"
    altered_result = run(altered)
    baseline = json.loads((ROOT / "expected_output.json").read_text())
    altered_rows = {x["dimension"]: x for x in altered_result["evidence_matrix"]}
    baseline_rows = {x["dimension"]: x for x in baseline["evidence_matrix"]}
    checks = {"manufacturer_conflict_changes_product_result": altered_rows["product_identification"]["status"] != baseline_rows["product_identification"]["status"], "material_does_not_upgrade_from_belief": altered_rows["material_content"]["status"] == "UNCERTAIN", "changed_record_hash_differs": altered_result["canonical_record_sha256"] != baseline["canonical_record_sha256"], "dimensions_remain_separate": len(altered_result["separation_preserved"]) == 7}
    result = {"tamper_controls": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if result["tamper_controls"] == "PASS" else 1)

if __name__ == "__main__": main()
