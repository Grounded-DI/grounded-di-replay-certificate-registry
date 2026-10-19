#!/usr/bin/env python3
"""Independent source-record recalculation for the FinanceWise replay.

This file intentionally does not import finance_core or any stage module.  It
recomputes the measured financial values and disposition from the canonical
JSON record, then compares selected fields with the generated outputs.
"""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

COLLECTIONS = ["bank_entries", "invoices", "payments", "ledger_entries", "ar", "ap", "debt", "covenants"]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def source_errors(data):
    company = data["company"]["entity_id"]
    errors = []
    for source in data.get("sources", []):
        if source.get("entity_id") not in (company, "SYNTH-LENDER-001"):
            errors.append({"record_id": source.get("source_id"), "kind": "ENTITY_BINDING_MISMATCH"})
    for collection in COLLECTIONS:
        for record in data.get(collection, []):
            if not record.get("source_id") or not record.get("source_location"):
                errors.append({"record_id": record.get("id"), "kind": "MISSING_SOURCE_BINDING"})
    return errors


def independent_resolution(data):
    base = data["reporting"]["base_currency"]
    duplicate_candidates = []
    groups = defaultdict(list)
    for payment in data.get("payments", []):
        key = (payment.get("date"), payment.get("amount"), payment.get("currency"), payment.get("counterparty"), payment.get("reference"))
        groups[key].append(payment["id"])
    for key, ids in groups.items():
        bank_matches = [b["id"] for b in data.get("bank_entries", []) if (b.get("date"), abs(b.get("amount", 0)), b.get("currency"), b.get("counterparty")) == (key[0], key[1], key[2], key[3])]
        if len(ids) > 1 or bank_matches:
            duplicate_candidates.append({"records": ids + bank_matches, "classification": "DUPLICATE_CANDIDATE" if len(ids) > 1 else "PROBABLE_MATCH"})

    conflicts = []
    for bank in data.get("bank_entries", []):
        if bank.get("amount", 0) <= 0 or bank.get("currency") != base:
            continue
        for invoice in data.get("invoices", []):
            if (bank.get("amount"), bank.get("currency"), bank.get("counterparty")) != (invoice.get("amount"), invoice.get("currency"), invoice.get("counterparty")):
                continue
            ar = [x for x in data.get("ar", []) if x.get("invoice_id") == invoice.get("id")]
            if ar and ar[0].get("status") == "OPEN":
                conflicts.append("/".join([bank["id"], invoice["id"], ar[0]["id"]]))
            if invoice.get("status", "").startswith("PAID") and not [p for p in data.get("payments", []) if p.get("reference") == invoice.get("id")]:
                conflicts.append(invoice["id"])
    missing = [x.get("id") for x in data.get("missing_records", [])]
    missing.extend(x["record_id"] for x in source_errors(data))
    return duplicate_candidates, conflicts, missing


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("run_dir")
    a = p.parse_args()
    data = load(a.input)
    run = Path(a.run_dir)
    resolution = independent_resolution(data)
    base = data["reporting"]["base_currency"]
    cash = sum(x.get("amount", 0) for x in data.get("bank_entries", []) if x.get("currency") == base)
    unsupported = [x.get("id") for x in data.get("bank_entries", []) if x.get("currency") != base]
    liabilities = sum(x.get("amount", 0) for x in data.get("ap", []) if x.get("currency") == base and x.get("status") == "OPEN")
    liabilities += sum(x.get("current_portion", 0) for x in data.get("debt", []) if x.get("currency") == base)
    ownership_missing = any(x.get("type") == "account_ownership_certificate" for x in data.get("missing_records", []))
    rule = data["covenants"][0]
    ratio = None if liabilities == 0 else round(cash / liabilities, 8)
    unresolved = list(resolution[2])
    unresolved.extend(resolution[1])
    unresolved.extend("UNSUPPORTED_CURRENCY:" + x for x in unsupported)
    if rule.get("reporting_date") != data["reporting"]["period_end"]:
        unresolved.append("REPORTING_DATE_MISMATCH")
    unauthorized = [x for x in rule.get("permitted_exclusions", []) if x not in data.get("authorized_exclusions", [])]
    unresolved.extend("UNAUTHORIZED_EXCLUSION:" + x for x in unauthorized)
    arithmetic = "UNDEFINED" if ratio is None else ("ABOVE_THRESHOLD" if ratio >= rule["minimum_ratio"] else "BELOW_THRESHOLD")
    disposition = "INSUFFICIENT_RECORD" if ratio is None else ("REVIEW_REQUIRED" if unresolved else ("COMPLIANT" if ratio >= rule["minimum_ratio"] else "NONCOMPLIANT"))
    expected = {
        "measured_cash": cash,
        "measured_current_liabilities": liabilities,
        "unsupported_currency_records": unsupported,
        "ownership_missing": ownership_missing,
        "duplicate_candidate_count": len(resolution[0]),
        "conflict_count": len(resolution[1]),
        "missing_foundation_count": len(resolution[2]),
        "ratio": ratio,
        "minimum_ratio": rule["minimum_ratio"],
        "arithmetic_result": arithmetic,
        "unresolved_items": unresolved,
        "disposition": disposition,
    }
    binder = load(run / "recordbinder.json")
    resolver = load(run / "transactionresolver.json")
    account = load(run / "accountingboundary.json")
    covenant = load(run / "covenantbridge.json")
    final = load(run / "final_chain.json")
    observed = {
        "measured_cash": account.get("measured_cash"),
        "measured_current_liabilities": account.get("measured_current_liabilities"),
        "unsupported_currency_records": account.get("unsupported_currency_records"),
        "ownership_missing": account.get("ownership_missing"),
        "duplicate_candidate_count": len(resolver.get("duplicate_candidates", [])),
        "conflict_count": len(resolver.get("conflicts", [])),
        "missing_foundation_count": len(resolver.get("missing_foundation", [])),
        "ratio": covenant.get("ratio"),
        "minimum_ratio": covenant.get("minimum_ratio"),
        "arithmetic_result": covenant.get("arithmetic_result"),
        "unresolved_items": covenant.get("unresolved_items"),
        "disposition": final.get("disposition"),
    }
    comparisons = {key: observed[key] == value for key, value in expected.items()}
    comparisons["binder_count"] = binder.get("bound_record_count") == sum(len(data.get(name, [])) for name in COLLECTIONS)
    passed = all(comparisons.values())
    result = {
        "schema": "financewise-independent-evaluator-v2",
        "status": "PASS" if passed else "FAIL",
        "imports_primary_stage_logic": False,
        "recalculation_source": "canonical synthetic source records",
        "calculated": expected,
        "observed": observed,
        "comparisons": comparisons,
        "input_sha256": hashlib.sha256(Path(a.input).read_bytes()).hexdigest(),
    }
    print(json.dumps(result, sort_keys=True, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
