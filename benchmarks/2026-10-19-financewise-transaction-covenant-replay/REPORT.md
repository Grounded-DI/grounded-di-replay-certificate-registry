# FinanceWise transaction-to-covenant replay report

## Final disposition

**`REVIEW_REQUIRED`**. The synthetic record measures cash activity of $128,000
and current liabilities of $32,000, producing a measured 4.00x ratio against
the supplied 1.50x threshold. Arithmetic alone does not resolve the covenant:
the required account-ownership certificate is missing, and the $120,000 receipt
conflicts with the invoice/AR status showing INV-1001 open.

RecordBinder preserved source IDs and locations. TransactionResolver preserved
the duplicate-looking payments, conflict, and missing foundation. AccountingBoundary
kept transaction identity, account ownership, invoice validity, revenue
recognition, cash availability, liability existence, and classification separate.
CovenantBridge preserved the numerator, denominator, date, exclusions, threshold,
source support, rounding, unresolved items, and non-inferences.

Two fresh canonical executions were identical. The independent evaluator passed
without importing stage logic. Integrity and archive checks passed. Altered
transaction, currency, date, status, duplicate, entity, covenant-exclusion,
missing-record, and downstream-injection controls were exercised.

This proves deterministic replay of the disclosed synthetic workflow and
preservation of missingness and conflict. It does not prove real financial
compliance, audit assurance, GAAP/IFRS or tax correctness, legal advice,
lending or investment suitability, fraud detection, real entity identity,
independent provenance, external verification, or production readiness.
