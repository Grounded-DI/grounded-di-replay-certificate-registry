# FinanceWise transaction-to-covenant replay report

## Final disposition

**`REVIEW_REQUIRED`**. The result is derived from the canonical synthetic
records. The measured cash is `128000`; current liabilities
are `32000`; the measured ratio is
`4.0`. The stage derives its threshold from the covenant
record and its unresolved items from record-level validation results.

## Revision controls

The former hash-change-only controls were replaced with fourteen actual mutated-input
pipeline executions plus one mutated-intermediate downstream execution. Each input
case writes a mutated record, reruns RecordBinder, TransactionResolver,
AccountingBoundary, and CovenantBridge, and asserts an outcome or preserved boundary.
Existing control names were preserved in `CONTROL_RESULTS.json`. The cases cover
amount, currency, reporting date, unsupported paid label, duplicate handling,
entity binding, unauthorized exclusion, missing evidence, and downstream injection.

## Independent verification

The independent evaluator does not import stage logic. It independently recalculates
base-currency cash, open AP, current debt, conflicts, missing records, reporting-date
mismatch, ratio, threshold comparison, and disposition from the synthetic source record,
then compares those values with generated stage outputs and the final chain.

Two fresh canonical executions were identical. The independent evaluator passed.
The manifest and archive checks passed. No remote write occurred during this rebuild.

## Evidence and non-claims

This proves only deterministic replay of the disclosed synthetic workflow and the
observed response of the disclosed mutated fixtures. It does not establish real
financial compliance, audit assurance, GAAP/IFRS or tax correctness, legal advice,
lending or investment suitability, fraud detection, real company/account identity,
independent fresh-generation provenance, external verification, or production readiness.
