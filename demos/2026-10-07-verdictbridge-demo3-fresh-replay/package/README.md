# Fresh local replay of VerdictBridge Demo 3

**Measured result: PASS.** October 7, 2026 (America/New_York; execution timestamps are October 8 UTC). This is a fresh replay of the existing benchmark, not a new benchmark. Public release candidate authorized for publication; replay automation remains paused. **Internal verification; unaffiliated review pending.**

Exactly the same declared output under the same frozen execution conditions, with receipts showing what actually ran, SHA-256 hashes, and direct byte comparisons. Material changes produce a specified changed result or refusal.

This framing applies only to the finite case, frozen artifacts and controls actually tested. All three fresh runs used the same input, source and recorded local environment. The historical receipt does not record its OS/interpreter, so equality of the full historical environment is UNKNOWN. Direct byte equality to the historical artifacts was nevertheless measured.

## Read first

- [Two-page report](Fresh_Replay_Report.pdf)
- [Measured verification and comparisons](verification/measured-results.json)
- [All fifteen canonical hashes](HASHES.md)
- [Commands, exit codes and timings](execution/commands.json)
- [Recorded environment](environment.json)
- [Fresh replay source and evidence](replay/)
- [Invalid hearsay export evidence](replay/invalid-hearsay-control/export-boundary-result.json)
- [Replay certificate](replay-certificate.json) and [checksum manifest](SHA256SUMS.txt)

## Observations

Three fresh evaluator processes: 64149, 64150, 64151. All five artifacts match each other and all three pinned historical counterparts directly, with zero byte differences. Strict liability, negligence and compensatory damages: DENY_SUMMARY_JUDGMENT; punitive damages: GRANT_SUMMARY_JUDGMENT; overall: GRANTED_IN_PART_DENIED_IN_PART. Sam Reed excluded, jury instruction coverage PASS, VerdictReady YES and export authorization true.

The inadmissible-hearsay candidate was substantively refused by the separate verifier (expected exit 2), and the export boundary refused before any export file open or write. Recorded invalid values: VerdictReady NO; authorization false; opens 0; bytes 0; inventory []. The verifier records L015 / F051-F054 / L020 and VB-D-EAUR, VERDICTREADY-GATE, EXPORT-GATE. The export boundary additionally records LEGAL_DISPOSITION_MISMATCH / VB-B-MOCC.

Seven prescribed tamper controls were freshly exercised on isolated copies. Each returned its expected class of integrity/substantive error. The deliberately missing export control tests missing-artifact detection; it is not evidence of substantive hearsay refusal. Oracle independence, baseline recalculation by the new evaluator, and forged-disposition export refusal also passed.

Differences from the pinned run receipts are limited to pid, started_at_unix_ns and finished_at_unix_ns. These variable fields are outside the canonical byte boundary. Evaluator, verifier, specification and preserved reference files are unchanged. No new model calls occurred.

## Provenance and limits

`pinned/` preserves the historical public ZIP and its extracted contents. Its recorded PASS labels and PDF concern the earlier execution. `replay/` contains this activation's fresh runs, unchanged runnable source and frozen input. Original reference evidence is evidence only; the evaluator was newly implemented for the earlier Demo 3, and its separate verifier is internal. No original engine execution, universal model determinism, unaffiliated validation, external certification or legal compliance is claimed.

Pin: ac3a8cd522718235d2a7154c728566614086a809. Public ZIP SHA-256: b504de22e948fd382fadb640781955668a1ff0f32b71aa93e4cea317e9fc12b9.

## Reproduce separately, without overwriting this evidence

Python 3.9+; standard library for core execution. From this directory:

```sh
python3 -B verify_package.py
python3 -B replay/source/verify.py
python3 -B pinned/VerdictBridge_Demo3_Public_v1/source/acceptance.py
python3 -B replay/source/reproduce.py /absolute/path/to/a-new-nonexistent-directory
python3 -B tools/compare_fresh.py /absolute/path/to/a-new-nonexistent-directory
```

The recorded activation used sequential commands with 120-second process-group timeouts and a lock. `execution/commands.json` records their exact arguments and observed exits. The machine-specific controller is omitted from this public derivative; use the portable commands above for a separate authorized replay and impose the same finite timeout. Do not run the original release-level verifier against the fresh replay folder, which lacks the old release-level report/certificate/manifest. `verify_package.py` verifies this delivered package without executing the benchmark.

The certificate binds every delivered file except itself and SHA256SUMS.txt; the manifest additionally binds the certificate. The final ZIP has an adjacent external SHA-256 sidecar, avoiding circular self-hashing. Checksums and the certificate are unsigned local records.

Preservation preflight initially read older staging files slowly. A parallel read-only diagnostic inventory reached its 20-second timeout; it ran no evaluator and was not an evidence-contract test. The primary preservation preflight completed, and no benchmark step timed out or failed unexpectedly. Existing evidence was hashed before and after; automation configuration is unchanged.

Next step: unaffiliated source and evidence review, with the reviewer recording their own observations and interests. No outreach has been performed.

## Public packaging provenance

This public derivative preserves every canonical run artifact, run receipt, frozen case/reference file, evaluator/verifier source, original pinned public archive and two-page PDF byte for byte. The PDF is the historical execution report and its local/unsent wording describes the state when it was prepared; it does not assert the current publication state.

Machine-specific path values in environment/command logs and temporary-path error messages are replaced with explicit placeholders. The raw local controller and unrelated local preservation inventory are omitted. PUBLIC-RELEASE-NOTES.json records changed/omitted files and binds the original local ZIP hash. Execution times, PIDs, outcomes and canonical hashes are unchanged. No new benchmark executions occurred during publication preparation. The internal certificate and manifest are regenerated for these public bytes; the public complete ZIP therefore has a different hash.

The original local ZIP and reviewer handoff remain unchanged and private. No conversational prompt or original-reference/mission.txt is included. This is a fresh replay of Demo 3, not a new benchmark.
