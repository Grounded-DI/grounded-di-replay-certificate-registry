# Published Demo 3 release: fresh local replay

**PASS for the bounded replay.** October 8, 2026 (America/New_York). This is the public derivative authorized for publication; replay automation remains paused. **Internal verification; unaffiliated review pending.** It is a fresh replay of the existing Demo 3 benchmark, not a new benchmark or unaffiliated validation.

## Source and provenance

Downloaded from commit `46903262313a164642aea4f6a496b398c2d120b6` in Grounded-DI/grounded-di-replay-certificate-registry, folder `demos/2026-10-07-verdictbridge-demo3-fresh-replay/`.

The received public ZIP SHA-256 is `8f401a26711b423055079423e766558e1b2ec82309bbc470d469969d5bd448cc`. Its checksum, all 127 manifest entries and 126 certificate bindings were verified before execution. `received/` retains the downloaded ZIP and unchanged extracted public release. Those nested reports/certificates describe prior executions, not this activation.

Four evidence layers remain distinct: preserved original references, the previously implemented local evaluator, its separate internal verifier, and measured fresh executions. No facts, rules, expected outcomes, source or canonical serialization were changed. No generative-model calls or original-engine execution occurred. No universal model determinism, external certification or legal compliance is claimed.

## Evidence index

- [Two-page visually reviewed report](Published_Replay_Report.pdf)
- [Measured results](verification/measured-results.json) and [all fifteen hashes](HASHES.md)
- [Recorded environment](environment.json) and [comparison with published environment](environment-comparison.json)
- [Commands, exits and timings](execution/commands.json)
- [Fresh source/specification/run folders](replay/)
- [Hearsay export boundary](replay/invalid-hearsay-control/export-boundary-result.json), [open audit](replay/invalid-hearsay-control/export-open-audit.json), [verifier refusal](replay/invalid-hearsay-control/verifier-refusal.json)
- [Acceptance controls](execution/acceptance-controls.stdout.txt)
- [Download receipt](verification/download-receipt.json), [preflight](verification/preflight-integrity.json), [preservation check](verification/preservation-after.json)
- [Replay certificate](replay-certificate.json) and [manifest](SHA256SUMS.txt)

## Measured outcomes

Exactly three new evaluator processes: 74180, 74181, 74182. They ran sequentially without overlap; all top-level benchmark steps had 120-second process-group timeouts and expected exit codes. The driver invoked the unchanged evaluator three times. Acceptance controls also exercise rule derivation/export functions, and are recorded separately from the three canonical evaluator executions.

Strict liability, negligence and compensatory damages: DENY_SUMMARY_JUDGMENT. Punitive damages: GRANT_SUMMARY_JUDGMENT. Overall: GRANTED_IN_PART_DENIED_IN_PART. Sam Reed: EXCLUDED_AND_NOT_USED. Jury instruction coverage PASS; VerdictReady YES; export authorization true.

All five canonical artifact types match across the three fresh runs, all three published runs and the three older pinned runs by SHA-256 and direct byte comparison (zero byte mismatches). The canonical ZIP entry metadata remains January 1, 1980. Real process IDs and timestamps remain outside the canonical archive in run receipts.

The hearsay candidate verifier returned the expected exit 2 for INADMISSIBLE_EVIDENCE_RELIANCE, rule L015 / F051-F054 / L020 and gates VB-D-EAUR, VERDICTREADY-GATE, EXPORT-GATE. The actual boundary additionally records LEGAL_DISPOSITION_MISMATCH / VB-B-MOCC. VerdictReady NO, authorization false, export opens 0, bytes written 0, final export inventory []. Both the empty open audit and actual output directory were checked by the unchanged verifier.

All seven tamper controls returned their prescribed class of failure: reference law, restored cost fact, wrong disposition, Reed in trace, missing export, forged receipt and ZIP byte change. The intentionally removed export tests completeness; it is not a substantive hearsay refusal. Oracle independence, baseline recalculation and forged-disposition export refusal passed. No unexplained crash or missing refusal result was counted as success.

## Differences and environmental comparability

Only pid, started_at_unix_ns and finished_at_unix_ns changed in the run receipts versus the published replay. Canonical bytes did not change. The new report, commands, environment timestamps and complete delivery archive necessarily differ.

All nine recorded comparison fields match: Python version, implementation, Python binary SHA-256, OS, release, architecture, locale, timezone names and selected environment variables. Current execution uses CPython 3.9.6 / Darwin 25.6.0 / arm64. Published executable path identity is UNKNOWN because it was redacted; the binary hashes match. Unrecorded machine state is not assessed; full historical environment identity is not inferred. These known scope limits are distinct from an unexpected replay failure.

## Reproduce into a new directory

Python 3.9+; standard library for core execution. Keep this evidence unchanged and select a nonexistent destination. Impose a 120-second timeout on each execution and do not overlap runs.

```sh
python3 -B verify_package.py
python3 -B replay/source/verify.py
python3 -B received/VerdictBridge_Demo3_Fresh_Replay_Public_v1/pinned/VerdictBridge_Demo3_Public_v1/source/acceptance.py
python3 -B replay/source/reproduce.py /absolute/path/to/new-destination
python3 -B tools/compare_fresh.py /absolute/path/to/new-destination
```

The first command checks package integrity without replay. The command log records exact arguments with explicit path redactions; the machine-specific controller is omitted. Do not use the older verify_release.py against the new reproduction folder; it expects the older release's report/manifest/certificate. Stop on unexpected FAIL/UNKNOWN and preserve the attempt.

The unsigned local certificate binds every delivered file except itself and SHA256SUMS.txt. The manifest additionally binds the certificate. The final ZIP hash is external, avoiding self-reference. Original local evidence, downloaded evidence and automation configuration were preserved.

Next concrete review step: inspect the environment comparison and fresh invalid-control evidence, then obtain an unaffiliated review of the exact package. No outreach was performed. The original measurement package was prepared locally; this derivative is authorized for publication.

## Public packaging provenance

This derivative preserves the canonical artifacts, truthful run receipts, frozen facts/rules, evaluator, substantive verifier, received published evidence and PDF byte for byte. The PDF describes the execution-time local/unpublished state. Logs and environment records have explicit machine-path redactions, documented in PUBLIC-RELEASE-NOTES.json; no execution outcomes, PIDs, timestamps or canonical hashes changed. The local controller and unrelated preservation inventory are omitted. Certificate and manifest bindings are regenerated for these public bytes. No benchmark was rerun during publication preparation. The original local evidence is unchanged.
