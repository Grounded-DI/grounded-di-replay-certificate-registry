#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run_modified(modifier):
    original = json.loads((ROOT / "input.json").read_text(encoding="utf-8"))
    modifier(original)
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "input.json"
        p.write_text(json.dumps(original), encoding="utf-8")
        r = subprocess.run([sys.executable, str(ROOT / "replay.py"), str(p)], capture_output=True, text=True, check=True)
        return json.loads(r.stdout)

def main():
    changed = run_modified(lambda d: d["propositions"][0].update({"authority_ids": ["SYNTH-AUTH-999"]}))
    overbroad = run_modified(lambda d: d["propositions"][2].update({"authority_ids": ["SYNTH-AUTH-999"]}))
    checks = {"missing_authority_routes_to_unresolved": "P-001" in changed["unresolved_propositions"], "disposition_remains_review": changed["disposition"] == "REVIEW_REQUIRED", "changed_fixture_changes_canonical_hash": changed["canonical_record_sha256"] != json.loads((ROOT / "expected_output.json").read_text())["canonical_record_sha256"], "overbroad_fixture_is_not_accepted_as_supported": "P-003" in overbroad["unresolved_propositions"]}
    result = {"tamper_controls": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if result["tamper_controls"] == "PASS" else 1)

if __name__ == "__main__":
    main()
