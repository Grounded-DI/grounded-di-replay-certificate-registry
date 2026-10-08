# VerdictBridge Demo 3 — standalone reproducibility specification

Case: `Lane v. Apex Industrial Tools, Inc.`
Variant: `VB-DEMO-0001-PUNITIVE-CONTROL`
Operator: Mark S. Weinstein / Grounded DI LLC.
Operator-provided production context: Grounded DI OS via FastPath 6.1 Sol - Medium.

## Reference and implementation boundaries

The five files in `original-reference/Run-2-*` are preserved reference evidence from `Verdictbridge_demo-2` at registry commit `8472b48470b6c35a3ad2778f0819f36d4ddaef1b`. Their exact digests are in `provenance.json` and the PDF. They are not executable original source. The evaluator and separate verifier in `source/` are new local implementations for this exact finite benchmark. The verifier imports no evaluator code. No original engine or native VerdictBridge reproduction is claimed.

## Frozen transformation

Start with the preserved original canonical input. Keep all 20 controlling rules, 58 facts, questions, procedure, admissibility rules, damages, and instructions except these replacements:

- **F037:** Apex marketing director Victor Hale rejected the proposed Zeta-9-specific warning recommended by Elena Cole. The record does not establish Hale’s reason for rejecting the proposed warning.
- **F038:** Hale’s authenticated internal email is Record Exhibit PX-005.
- **F039:** PX-005 is an admissible statement of a party opponent.
- **F040:** PX-005 states that Apex would retain the shorter warning despite the engineering recommendation. PX-005 does not state that the decision was made to avoid a per-unit cost increase and does not state any other reason for the decision.

F038/F039 are exact restatements; only F037/F040 fact text changes. Change the case ID and encode the expected dispositions before execution. Keep F035/F036 and F051–F054 unchanged. Add no substitute punitive evidence. No external facts or authorities enter this benchmark.

## Expected selective result

| Field | Required result |
|---|---|
| Strict liability | DENY_SUMMARY_JUDGMENT |
| Negligence | DENY_SUMMARY_JUDGMENT |
| Compensatory damages | DENY_SUMMARY_JUDGMENT |
| Punitive damages | GRANT_SUMMARY_JUDGMENT |
| Overall motion | GRANTED_IN_PART_DENIED_IN_PART |
| Sam Reed | EXCLUDED_AND_NOT_USED |
| Jury instruction coverage | PASS |
| Appellate review / FilingReady | NOT_APPLICABLE |
| VerdictReady | YES |
| Export authorized | true |

L007 still permits negligence based on the knowing rejection. For this stipulated exact case, the removed affirmative cost motive supplies no L010 conscious-disregard predicate, and no substitute is introduced. L015/F051–F054 exclude Reed; L020 blocks readiness for reliance on inadmissible evidence. L001/L008/L018 leave competing admissible experts to the jury. This is the declared finite-case operationalization, not actual-jurisdiction law.

All original major gate expectations remain: SYSTEM-GATE, INPUT-NORM, VB-C-VNCI, VB-D-EAUR, VB-B-MOCC, VB-A-CESMS, VB-E-SRAG, VB-F-DESR, VB-G-JICI, REPLAY-GATE, VERDICTREADY-GATE, and EXPORT-GATE PASS; LEGAL-KERNEL NOT_ACTIVE; VB-H-ARCR NOT_APPLICABLE. ReplayDivergence and StateTransitionMismatch must be zero. Correct dismissal of punitive damages is not a failed gate.

Preserve the original surviving instruction mappings except omit the no-longer-required `punitive_damages -> MI-PUN-101`. Product identification, strict liability, negligence, specific causation, competing experts, and each compensatory category retain the mappings specified in the frozen input and verifier.

## Three-run and five-hash contract

Launch three separate evaluator processes, each from the same frozen `valid-case/01_canonical_input.json`, into fresh Run-A, Run-B, and Run-C folders. Each process freshly generates:

1. `01_canonical_input.json`
2. `02_normalized_record.csv`
3. `03_gate_matrix.json`
4. `04_verdictbridge_assessment.txt`
5. `canonical_run.zip`

Do not copy generated artifacts between runs. Require three-way direct byte equality and three-way SHA-256 equality for all five. JSON uses sorted compact UTF-8 keys without final LF; CSV uses standard quoting and LF; assessment text has final LF. ZIP contains only the four records in lexicographic order, ZIP_STORED, fixed 1980-01-01 timestamps, UNIX regular-file mode 0644, and no comments or extra fields.

Keep `run_receipt.json` outside the canonical ZIP. Receipts include benchmark name, case ID, run number 1/2/3, total runs 3, all five measured hashes, record mismatches, numeric error, and verification result. Also preserve process/time provenance and source/input identity. Never prepopulate or invent hashes.

## Invalid control and measured refusal

Create an analysis that retains punitive damages using F051: “I heard Apex always knew the machine was dangerous.” The separate verifier must reject it. The local writer must independently refuse export. Record failed rules/gates, VerdictReady NO, export false, file-open attempts, bytes written, and final export inventory. Required refused-control outcome: zero export opens, zero bytes, empty export inventory. Diagnostic evidence is outside the export directory.

## Acceptance and deliverables

Recompute exact transformation, preserved rules, selective outcomes, Reed exclusion, readiness/export, surviving instructions, reference hashes, all generated hashes, ZIP contents/metadata, and direct byte equality. Compare preserved original results with the new case: only punitive damages and overall motion change. Reject altered evidence. Do not infer success from saved PASS text.

Deliver source, five references, frozen input, three runs/receipts, invalid-control evidence, comparisons, README, unsigned local certificate, manifest, PDF with complete hashes, and ZIP. Visually review every PDF page. Preserve original local evidence separately; the conversational prompt is not included in this public release.

PASS requires every condition above. FAIL denotes a violated condition; UNKNOWN denotes insufficient evidence. Matching executions establish repeatability only for this exact new local evaluator and frozen record. No universal model determinism, original engine execution, native reproduction, or external attestation is claimed.
