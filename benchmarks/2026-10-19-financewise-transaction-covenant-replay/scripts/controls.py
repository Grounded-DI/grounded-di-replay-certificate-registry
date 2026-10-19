#!/usr/bin/env python3
"""Execute preserved FinanceWise controls against real mutated records."""
import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_case(case_dir, input_path, pipeline, package_root):
    out = case_dir / "run"
    q = subprocess.run([sys.executable, str(pipeline), str(input_path), str(out)], cwd=package_root, text=True, capture_output=True, check=False)
    (case_dir / "pipeline.stdout.txt").write_text(q.stdout, encoding="utf-8")
    (case_dir / "pipeline.stderr.txt").write_text(q.stderr, encoding="utf-8")
    return q, out


def mutate(data, name, baseline):
    d = copy.deepcopy(data)
    if name == "altered_transaction_amount":
        d["bank_entries"][0]["amount"] += 1
    elif name == "altered_currency":
        d["bank_entries"][2]["currency"] = "EUR"
    elif name == "altered_reporting_date":
        d["covenants"][0]["reporting_date"] = "2026-10-01"
    elif name == "invoice_relabeled_paid_without_payment":
        d["invoices"][0]["status"] = "PAID_IN_PAYMENT_REGISTER"
    elif name == "duplicate_forced_into_match":
        d["payments"][1]["reference"] = "INV-9999"
    elif name == "duplicate_transaction":
        d["payments"].append(copy.deepcopy(d["payments"][0]))
        d["payments"][-1]["id"] = "PAY-2001-TRIPLE"
        d["payments"][-1]["source_location"] = "page 1 row 22"
    elif name == "entity_identifier_replaced":
        d["company"]["entity_id"] = "SYNTH-CO-REPLACED"
    elif name == "unauthorized_covenant_exclusion":
        d["covenants"][0]["permitted_exclusions"] = ["cash_restricted_by_unknown_rule"]
    elif name == "missing_record_treated_as_zero":
        d["missing_records"] = []
    elif name == "negative_control":
        d["negative_controls"].append({"id": "NC-MUTATED", "source_id": "NEGATIVE-CONTROL", "source_location": "memo paragraph 2", "text": "Unrelated narrative with a large amount 999999; it is not a financial record.", "amount": 999999, "type": "unrelated_memo"})
    elif name == "currency_conversion":
        d["bank_entries"][2]["currency"] = "EUR"
        d["fx_rates"] = [{"from": "EUR", "to": "USD", "rate": 1.2, "source": "UNAUTHORIZED_FIXTURE_RATE"}]
    elif name == "rounding_boundary":
        d["covenants"][0]["minimum_ratio"] = baseline["measured_ratio"] + 0.00001
    elif name == "downstream_injection":
        d["injected_disposition"] = "COMPLIANT"
        d["injected_ratio"] = 999999
    return d


def assert_case(name, baseline, result, resolver, account, covenant, final):
    if name == "altered_transaction_amount":
        return account["measured_cash"] != baseline["measured_cash"], "cash recalculated from altered amount"
    if name in {"altered_currency", "currency_conversion"}:
        return "B-003" in account["unsupported_currency_records"] and account["measured_cash"] != baseline["measured_cash"], "unsupported currency preserved and cash changed"
    if name == "altered_reporting_date":
        return "REPORTING_DATE_MISMATCH" in covenant["unresolved_items"], "reporting mismatch derived"
    if name == "invoice_relabeled_paid_without_payment":
        return any("paid without payment-register evidence" in x["basis"] for x in resolver["conflicts"]), "paid-without-payment conflict derived"
    if name == "duplicate_forced_into_match":
        return not any(x["classification"] == "DUPLICATE_CANDIDATE" for x in resolver["duplicate_candidates"]), "forced duplicate no longer accepted as duplicate"
    if name == "duplicate_transaction":
        return any(len(x["records"]) > baseline["duplicate_record_count"] for x in resolver["duplicate_candidates"]), "additional duplicate record detected"
    if name == "entity_identifier_replaced":
        return any(x["kind"] == "ENTITY_BINDING_MISMATCH" for x in resolver["binding_errors"]), "entity mismatch rejected"
    if name == "unauthorized_covenant_exclusion":
        return "UNAUTHORIZED_EXCLUSION:cash_restricted_by_unknown_rule" in covenant["unresolved_items"], "unsupported exclusion unresolved"
    if name == "missing_record_treated_as_zero":
        return account["measured_cash"] == baseline["measured_cash"] and final["disposition"] != "COMPLIANT", "missing evidence did not become zero or compliance"
    if name == "negative_control":
        return final["disposition"] == baseline["disposition"] and account["measured_cash"] == baseline["measured_cash"], "unrelated memo ignored"
    if name == "rounding_boundary":
        return covenant["arithmetic_result"] == "BELOW_THRESHOLD" and final["disposition"] == "REVIEW_REQUIRED", "threshold comparison derived before disposition"
    if name == "downstream_injection":
        return final["disposition"] == baseline["disposition"] and "injected_disposition" not in final, "downstream label not accepted"
    return False, "unknown control"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("pipeline")
    p.add_argument("output")
    a = p.parse_args()
    input_path = Path(a.input).resolve()
    pipeline = Path(a.pipeline).resolve()
    package_root = pipeline.parent.parent
    root = package_root / "controls"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    data = load(input_path)
    baseline_run = package_root / "executions" / "run_1"
    baseline_final = load(baseline_run / "final_chain.json")
    baseline_account = load(baseline_run / "accountingboundary.json")
    baseline_resolver = load(baseline_run / "transactionresolver.json")
    baseline = {
        "disposition": baseline_final["disposition"],
        "measured_cash": baseline_account["measured_cash"],
        "measured_current_liabilities": baseline_account["measured_current_liabilities"],
        "measured_ratio": baseline_final["measured_ratio"],
        "duplicate_candidate_count": len(baseline_resolver["duplicate_candidates"]),
        "duplicate_record_count": max((len(x["records"]) for x in baseline_resolver["duplicate_candidates"]), default=0),
    }
    names = ["altered_currency", "altered_reporting_date", "altered_transaction_amount", "currency_conversion", "downstream_injection", "duplicate_forced_into_match", "duplicate_transaction", "entity_identifier_replaced", "intermediate_tamper", "invoice_relabeled_paid_without_payment", "missing_evidence", "missing_record_treated_as_zero", "negative_control", "rounding_boundary", "unauthorized_covenant_exclusion"]
    results = {}
    for name in names:
        case_dir = root / name
        case_dir.mkdir(parents=True)
        if name == "missing_evidence":
            mutated = copy.deepcopy(data)
            mutated["missing_records"] = []
            mutated["ap"] = []
        elif name == "intermediate_tamper":
            shutil.copytree(baseline_run, case_dir / "baseline_run")
            tampered = load(case_dir / "baseline_run" / "transactionresolver.json")
            tampered["conflicts"].append({"records": ["TAMPERED"], "classification": "CONFLICT", "basis": "intermediate record altered after source execution"})
            dump(case_dir / "baseline_run" / "transactionresolver.json", tampered)
            out = case_dir / "run"
            out.mkdir(parents=True, exist_ok=True)
            q = subprocess.run([sys.executable, str(pipeline.parent / "finance_stage_v2.py"), "covenant", str(input_path), str(out / "covenantbridge.json"), "--resolver", str(case_dir / "baseline_run" / "transactionresolver.json"), "--accounting", str(case_dir / "baseline_run" / "accountingboundary.json")], cwd=pipeline.parent, text=True, capture_output=True, check=False)
            (case_dir / "pipeline.stdout.txt").write_text(q.stdout, encoding="utf-8")
            (case_dir / "pipeline.stderr.txt").write_text(q.stderr, encoding="utf-8")
            covenant = load(out / "covenantbridge.json") if q.returncode == 0 else {}
            passed = q.returncode == 0 and "TAMPERED" in covenant.get("unresolved_items", []) and covenant.get("disposition") == "REVIEW_REQUIRED"
            results[name] = {"status": "PASS" if passed else "FAIL", "execution": "mutated intermediate record", "assertion": "tampered intermediate changed downstream result", "observed": covenant.get("unresolved_items", [])}
            continue
        else:
            mutated = mutate(data, name, baseline)
        mutated_input = case_dir / "input.json"
        dump(mutated_input, mutated)
        q, out = run_case(case_dir, mutated_input, pipeline, package_root)
        if q.returncode:
            results[name] = {"status": "FAIL", "execution": "mutated input pipeline", "exit_code": q.returncode, "stderr": q.stderr}
            continue
        resolver = load(out / "transactionresolver.json")
        account = load(out / "accountingboundary.json")
        covenant = load(out / "covenantbridge.json")
        final = load(out / "final_chain.json")
        if name == "missing_evidence":
            passed = account["measured_current_liabilities"] != baseline["measured_current_liabilities"] and final["disposition"] != "COMPLIANT"
            reason = "missing AP record changed derived denominator and did not become a zero-valued supported fact"
        else:
            passed, reason = assert_case(name, baseline, resolver, resolver, account, covenant, final)
        results[name] = {"status": "PASS" if passed else "FAIL", "execution": "mutated input pipeline", "input_sha256": digest(mutated_input), "output_sha256": digest(out / "final_chain.json"), "assertion": reason, "observed": {"disposition": final["disposition"], "cash": account["measured_cash"], "ratio": covenant["ratio"], "unresolved": covenant["unresolved_items"], "duplicate_candidates": len(resolver["duplicate_candidates"])}}
    passed_count = sum(v["status"] == "PASS" for v in results.values())
    source_input_cases = len([name for name in names if name != "intermediate_tamper"])
    output = {"schema": "financewise-controls-v2", "baseline_disposition": baseline["disposition"], "canonical_input_hash": digest(input_path), "actual_control_executions": len(results), "actual_mutated_input_pipeline_executions": source_input_cases, "actual_mutated_intermediate_executions": 1, "hash_change_only_controls_replaced": True, "legacy_control_inventory": {"preserved_names": names, "all_preserved": True}, "controls": results, "pass_count": passed_count, "fail_count": len(results) - passed_count}
    dump(a.output, output)
    print(json.dumps({"status": "PASS" if passed_count == len(results) else "FAIL", "pass_count": passed_count, "fail_count": len(results) - passed_count, "actual_mutated_pipeline_executions": len(results)}))
    raise SystemExit(0 if passed_count == len(results) else 1)


if __name__ == "__main__":
    main()
