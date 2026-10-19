import json
from collections import defaultdict
from pathlib import Path

COLLECTIONS = ["bank_entries", "invoices", "payments", "ledger_entries", "ar", "ap", "debt", "covenants"]

def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def fragment(record):
    return json.dumps(record, sort_keys=True, separators=(",", ":"))

def source_bindings(data):
    company_id = data["company"]["entity_id"]
    errors = []
    for source in data.get("sources", []):
        if source.get("entity_id") not in (company_id, "SYNTH-LENDER-001"):
            errors.append({"record_id": source.get("source_id"), "kind": "ENTITY_BINDING_MISMATCH"})
    bindings = []
    for collection in COLLECTIONS:
        for record in data.get(collection, []):
            binding = {
                "record_id": record.get("id"),
                "source_id": record.get("source_id"),
                "source_location": record.get("source_location"),
                "source_fragment": fragment(record),
                "date": record.get("date", record.get("issue_date")),
                "posting_date": record.get("posting_date"),
                "payment_date": record.get("date") if str(record.get("id", "")).startswith("PAY-") else None,
                "amount": record.get("amount", record.get("principal", record.get("current_portion"))),
                "currency": record.get("currency", data["reporting"]["base_currency"]),
                "counterparty": record.get("counterparty"),
                "account": record.get("account", record.get("account_id")),
            }
            if not binding["source_id"] or not binding["source_location"]:
                errors.append({"record_id": record.get("id"), "kind": "MISSING_SOURCE_BINDING"})
            bindings.append(binding)
    return bindings, errors

def resolve(data):
    base = data["reporting"]["base_currency"]
    bindings, binding_errors = source_bindings(data)
    groups = defaultdict(list)
    for payment in data.get("payments", []):
        key = (payment.get("date"), payment.get("amount"), payment.get("currency"), payment.get("counterparty"), payment.get("reference"))
        groups[key].append(payment["id"])
    duplicates = []
    for key, ids in groups.items():
        bank_matches = [b["id"] for b in data.get("bank_entries", []) if (b.get("date"), abs(b.get("amount", 0)), b.get("currency"), b.get("counterparty")) == (key[0], key[1], key[2], key[3])]
        if len(ids) > 1 or bank_matches:
            duplicates.append({"records": ids + bank_matches, "classification": "DUPLICATE_CANDIDATE" if len(ids) > 1 else "PROBABLE_MATCH", "basis": "date, amount, currency, counterparty, and reference comparison"})
    conflicts = []
    for bank in data.get("bank_entries", []):
        if bank.get("amount", 0) <= 0 or bank.get("currency") != base:
            continue
        for invoice in data.get("invoices", []):
            same = bank.get("amount") == invoice.get("amount") and bank.get("currency") == invoice.get("currency") and bank.get("counterparty") == invoice.get("counterparty")
            if not same:
                continue
            ar = [x for x in data.get("ar", []) if x.get("invoice_id") == invoice.get("id")]
            if ar and ar[0].get("status") == "OPEN":
                conflicts.append({"records": [bank["id"], invoice["id"], ar[0]["id"]], "classification": "CONFLICT", "basis": "bank receipt and AR-open record disagree"})
            if invoice.get("status", "").startswith("PAID") and not [p for p in data.get("payments", []) if p.get("reference") == invoice.get("id")]:
                conflicts.append({"records": [invoice["id"]], "classification": "CONFLICT", "basis": "invoice marked paid without payment-register evidence"})
    missing = [{"records": [x.get("id")], "classification": "MISSING_FOUNDATION", "basis": x.get("reason", "record not supplied")} for x in data.get("missing_records", [])]
    missing.extend({"records": [x["record_id"]], "classification": x["kind"], "basis": "source/entity binding validation"} for x in binding_errors)
    return {"normalized_records": bindings, "duplicate_candidates": duplicates, "conflicts": conflicts, "missing_foundation": missing, "binding_errors": binding_errors, "status": "REVIEW_REQUIRED" if conflicts or missing else "PASS"}

def account(data, resolution):
    base = data["reporting"]["base_currency"]
    unsupported = [x for x in data.get("bank_entries", []) if x.get("currency") != base]
    cash = sum(x.get("amount", 0) for x in data.get("bank_entries", []) if x.get("currency") == base)
    liabilities = sum(x.get("amount", 0) for x in data.get("ap", []) if x.get("currency") == base and x.get("status") == "OPEN")
    liabilities += sum(x.get("current_portion", 0) for x in data.get("debt", []) if x.get("currency") == base)
    ownership_missing = any(x.get("type") == "account_ownership_certificate" for x in data.get("missing_records", []))
    items = [
        {"proposition": "transaction identity", "status": "SUPPORTED_WITH_CONFLICT" if resolution["conflicts"] else "SUPPORTED"},
        {"proposition": "account ownership", "status": "MISSING" if ownership_missing else "SUPPORTED"},
        {"proposition": "invoice validity", "status": "SUPPORTED_AS_RECORD_ONLY"},
        {"proposition": "revenue recognition", "status": "UNRESOLVED"},
        {"proposition": "cash availability", "status": "MEASURED_BUT_OWNERSHIP_UNRESOLVED" if ownership_missing else "MEASURED", "amount": cash},
        {"proposition": "liability existence", "status": "SUPPORTED_FOR_LISTED_ITEMS", "amount": liabilities},
        {"proposition": "financial-statement classification", "status": "UNRESOLVED"},
    ]
    status = "REVIEW_REQUIRED" if ownership_missing or unsupported or resolution["conflicts"] or resolution["missing_foundation"] else "PASS"
    return {"measured_cash": cash, "measured_current_liabilities": liabilities, "unsupported_currency_records": [x.get("id") for x in unsupported], "ownership_missing": ownership_missing, "items": items, "boundaries": ["transaction identity != account ownership", "invoice validity != revenue recognition", "cash availability != covenant compliance", "liability existence != financial-statement classification"], "status": status}

def covenant(data, resolution, accounting):
    rule = data["covenants"][0]
    ratio = None if accounting["measured_current_liabilities"] == 0 else accounting["measured_cash"] / accounting["measured_current_liabilities"]
    unresolved = [x["records"][0] for x in resolution["missing_foundation"]]
    unresolved += ["/".join(x["records"]) for x in resolution["conflicts"]]
    unresolved += ["UNSUPPORTED_CURRENCY:" + x for x in accounting["unsupported_currency_records"]]
    if rule.get("reporting_date") != data["reporting"]["period_end"]:
        unresolved.append("REPORTING_DATE_MISMATCH")
    unauthorized = [x for x in rule.get("permitted_exclusions", []) if x not in data.get("authorized_exclusions", [])]
    unresolved += ["UNAUTHORIZED_EXCLUSION:" + x for x in unauthorized]
    arithmetic = "UNDEFINED" if ratio is None else ("ABOVE_THRESHOLD" if ratio >= rule["minimum_ratio"] else "BELOW_THRESHOLD")
    if ratio is None:
        disposition = "INSUFFICIENT_RECORD"
    elif unresolved:
        disposition = "REVIEW_REQUIRED"
    elif ratio >= rule["minimum_ratio"]:
        disposition = "COMPLIANT"
    else:
        disposition = "NONCOMPLIANT"
    return {"covenant_id": rule["id"], "reporting_date": data["reporting"]["period_end"], "covenant_reporting_date": rule.get("reporting_date"), "numerator": {"name": rule["numerator"], "measured_usd": accounting["measured_cash"], "ownership_status": "MISSING" if accounting["ownership_missing"] else "SUPPORTED"}, "denominator": {"name": rule["denominator"], "measured_usd": accounting["measured_current_liabilities"]}, "permitted_exclusions": rule.get("permitted_exclusions", []), "unauthorized_exclusions": unauthorized, "ratio": None if ratio is None else round(ratio, 8), "minimum_ratio": rule["minimum_ratio"], "arithmetic_result": arithmetic, "unresolved_items": unresolved, "disposition": disposition}
