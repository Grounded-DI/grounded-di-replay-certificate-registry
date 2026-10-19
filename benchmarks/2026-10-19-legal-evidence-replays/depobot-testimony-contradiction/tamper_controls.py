#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def main():
    d = json.loads((ROOT / "input.json").read_text())
    d["transcript"][1]["answer"] = "No, I did not perform any work at the South Plant."
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "input.json"; p.write_text(json.dumps(d))
        r = subprocess.run([sys.executable, str(ROOT / "replay.py"), str(p)], capture_output=True, text=True, check=True)
        changed = json.loads(r.stdout)
    original = json.loads((ROOT / "expected_output.json").read_text())
    checks = {"altered_transcript_changes_canonical_hash": changed["canonical_record_sha256"] != original["canonical_record_sha256"], "original_direct_contradiction_remains_recorded": any(x["id"] == "C-001" for x in original["findings"]), "changed_record_is_not_silently_identical": changed != original}
    result = {"tamper_controls": "PASS" if all(checks.values()) else "FAIL", "checks": checks}
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if result["tamper_controls"] == "PASS" else 1)

if __name__ == "__main__": main()
