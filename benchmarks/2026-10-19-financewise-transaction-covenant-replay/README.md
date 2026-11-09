# FinanceWise transaction-to-covenant replay

Local closed-world replay using synthetic records only. Stage outputs derive
bindings, duplicates, conflicts, missing foundations, arithmetic, threshold
comparison, and final disposition from the canonical input and specification.

## Related FinanceWise research

The [FinanceWise — Auditable Market Review](https://github.com/Grounded-DI/financewise-auditable-market-review) repository publishes a 23-page, source-bounded comparison of FinanceWise's financial research and evidence-control approach with the J.P. Morgan 2026 Mid-Year Outlook. It addresses evidence categories, separate time-horizon conditions, corrections, lineage, and reproducibility. The market-review report and this synthetic covenant replay are **different evidence artifacts**: this benchmark tests its disclosed transaction-to-covenant workflow, not the entire proprietary FWO formula architecture.

Final disposition: `REVIEW_REQUIRED`. Measured cash: `128000`;
current liabilities: `32000`; ratio: `4.0`.
The package includes two canonical replays, an independent source-recalculation
evaluator, fourteen actual mutated-input pipeline executions, one mutated
intermediate-record execution, and the preserved negative, currency, rounding,
downstream-injection, and legacy-control tests.

This is not real financial compliance, audit assurance, GAAP/IFRS correctness,
tax correctness, legal advice, fraud detection, real entity identification,
independent provenance, external verification, or production deployment.
