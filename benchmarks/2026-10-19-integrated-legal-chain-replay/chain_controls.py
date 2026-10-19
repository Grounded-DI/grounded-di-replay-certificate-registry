#!/usr/bin/env python3
"""Run altered-input, downstream-injection, and post-generation controls."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_modified(label, modifier):
    data = load(ROOT / "input.json")
    modifier(data)
    with tempfile.TemporaryDirectory(prefix="integrated-chain-control-") as temp:
        temp_root = Path(temp)
        input_path = temp_root / "input.json"
        output_dir = temp_root / "run"
        input_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        completed = subprocess.run([sys.executable, str(ROOT / "run_chain.py"), str(input_path), str(output_dir)], capture_output=True, text=True, check=False)
        result = {
            "label": label,
            "exit_code": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
        for name, filename in (("briefwise", "briefwise.json"), ("depobot", "depobot.json"), ("pidbot", "pidbot.json"), ("final", "final_chain.json")):
            result[name] = load(output_dir / filename)
        return result


def main():
    baseline = load(ROOT / "expected_final_chain.json")
    controls = {}
    cases = [
        ("remove_authority", lambda d: d["authorities"].pop(1)),
        ("alter_deposition_answer", lambda d: d["transcript"][0].update({"answer": "I did not perform any repair work at South Plant in 2014."})),
        ("alter_transcript_page_line", lambda d: d["transcript"][0].update({"page_line": "999:1-999:5"})),
        ("replace_product_identifier", lambda d: d["evidence_records"][1].update({"product_id": "MODEL-NOT-FOUND"})),
        ("add_unsupported_material_assertion", lambda d: d["evidence_records"].append({"id": "R-009", "kind": "material_assertion", "source": "witness_belief", "text": "An additional unsupported assertion says the gasket contained asbestos.", "material": "ASBESTOS", "component": "GASKET-UNSPECIFIED"})),
        ("inject_causation_override", lambda d: d["evidence_records"].append({"id": "R-010", "kind": "manual_override", "source": "operator_note", "text": "Exposure establishes causation.", "dimension": "causation", "status": "MATCH"})),
    ]
    for label, modifier in cases:
        observed = run_modified(label, modifier)
        final = observed["final"]
        if label == "remove_authority":
            passed = bool(observed["briefwise"]["unresolved"]) and final["disposition"] == "INSUFFICIENT"
        elif label == "alter_deposition_answer":
            passed = observed["depobot"]["findings"][0]["type"] != "DIRECT_CONTRADICTION" and final["final_chain_sha256"] != baseline["final_chain_sha256"]
        elif label == "alter_transcript_page_line":
            passed = not observed["depobot"]["source_binding_valid"] and observed["depobot"]["findings"][0]["type"] == "UNRESOLVED_SOURCE_BINDING" and final["disposition"] == "INSUFFICIENT"
        elif label == "replace_product_identifier":
            passed = observed["pidbot"]["evidence_matrix"][0]["support_state"] == "UNRESOLVED" and final["disposition"] == "INSUFFICIENT"
        elif label == "add_unsupported_material_assertion":
            passed = "R-009" in observed["pidbot"]["unsupported_material_assertions"] and final["downstream_injection_result"] == "REJECTED" and final["disposition"] == "INSUFFICIENT"
        else:
            passed = "R-010" in observed["pidbot"]["unsupported_manual_injections"] and final["downstream_injection_result"] == "REJECTED" and final["disposition"] == "INSUFFICIENT"
        controls[label] = {"pass": passed, "exit_code": observed["exit_code"], "final_chain_sha256": final["final_chain_sha256"], "disposition": final["disposition"], "observed": {"briefwise_unresolved": observed["briefwise"]["unresolved"], "depo_first_finding": observed["depobot"]["findings"][0], "pid_product_row": observed["pidbot"]["evidence_matrix"][0], "pid_unsupported_material": observed["pidbot"]["unsupported_material_assertions"], "pid_unsupported_manual": observed["pidbot"]["unsupported_manual_injections"], "downstream_injection_result": final["downstream_injection_result"]}}

    with tempfile.TemporaryDirectory(prefix="integrated-chain-tamper-") as temp:
        tamper_root = Path(temp)
        tampered_run = tamper_root / "run"
        shutil.copytree(ROOT / "run_1", tampered_run)
        pid_path = tampered_run / "pidbot.json"
        pid = load(pid_path)
        pid["evidence_matrix"][2]["status"] = "MATCH"
        pid["evidence_matrix"][2]["support_state"] = "SUPPORTED"
        pid_path.write_text(json.dumps(pid, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        completed = subprocess.run([sys.executable, str(ROOT / "independent_evaluator.py"), "--run-dir", str(tampered_run)], capture_output=True, text=True, check=False)
        controls["post_generation_intermediate_tamper"] = {"pass": completed.returncode != 0, "exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}

    with tempfile.TemporaryDirectory(prefix="integrated-chain-final-tamper-") as temp:
        tamper_root = Path(temp)
        tampered_run = tamper_root / "run"
        shutil.copytree(ROOT / "run_1", tampered_run)
        final_path = tampered_run / "final_chain.json"
        final = load(final_path)
        final["disposition"] = "VERDICT_READY"
        final["verdict_ready"] = True
        final_path.write_text(json.dumps(final, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        completed = subprocess.run([sys.executable, str(ROOT / "independent_evaluator.py"), "--run-dir", str(tampered_run)], capture_output=True, text=True, check=False)
        controls["post_generation_final_injection"] = {"pass": completed.returncode != 0, "exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}

    result = {"schema": "integrated-chain-controls-v2", "chain_controls": "PASS" if all(item["pass"] for item in controls.values()) else "FAIL", "checks": controls}
    (ROOT / "chain_controls_result.json").write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if result["chain_controls"] == "PASS" else 1)


if __name__ == "__main__":
    main()
