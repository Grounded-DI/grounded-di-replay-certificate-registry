# Demo 3 - October 8 replay of the published release

**PASS within the stated finite scope. Internal verification; unaffiliated review pending.** This is a fresh replay of the existing Demo 3 benchmark, not a new benchmark.

[Two-page PDF](package/Published_Replay_Report.pdf) · [Complete public ZIP](VerdictBridge_Demo3_Published_Replay_Public_v1.zip) · [ZIP SHA-256](VerdictBridge_Demo3_Published_Replay_Public_v1.zip.sha256) · [Runnable package and instructions](package/README.md)

The release pinned to commit `46903262313a164642aea4f6a496b398c2d120b6` was downloaded and verified before execution. Three fresh evaluator processes reproduced all five canonical artifacts byte for byte against the published evidence. The declared selective result, Sam Reed exclusion, jury instruction coverage and VerdictReady/export behavior passed the separate internal verifier.

The hearsay control refused export with VerdictReady NO, export authorization false, zero file opens, zero bytes written and an empty inventory. All seven prescribed tamper controls were rejected for their expected reasons. No unrelated crash was counted as substantive refusal.

All nine recorded environment comparison fields matched. The published executable path was redacted, and unrecorded machine state remains unestablished. This is recorded-field comparability, not a claim of complete historical machine-state identity.

## Artifact boundary

Canonical ZIP metadata remains January 1, 1980. Truthful execution timestamps and process IDs remain in separate receipts. Canonical artifacts matched; fresh receipts and the complete delivery ZIP are expected to differ.

## Evidence

- [Measured results](package/verification/measured-results.json) and [all fifteen hashes](package/HASHES.md)
- [Environment comparison](package/environment-comparison.json) and [current environment](package/environment.json)
- [Fresh runs, unchanged source and frozen specification](package/replay/)
- [Invalid-control evidence](package/replay/invalid-hearsay-control/) and [tamper results](package/execution/acceptance-controls.stdout.txt)
- [Commands and exits](package/execution/commands.json), [certificate](package/replay-certificate.json), [manifest](package/SHA256SUMS.txt)
- [Public derivative notes](package/PUBLIC-RELEASE-NOTES.json)

Preserved reference evidence, the previously implemented evaluator, separate internal verification and measured fresh executions are distinct layers. No original-engine execution, universal model determinism, external certification or legal compliance is claimed. The unchanged PDF describes the execution-time local/unpublished state.

Public ZIP SHA-256:

```text
6e5399378479d8e7dc030f6c9139b93449978fd5cf57b39c5055e8eb4f05c5a6
```

Private machine paths were replaced with explicit placeholders in five records; the machine-specific controller and unrelated local preservation inventory are omitted. Canonical artifacts, run receipts, frozen facts/rules, evaluator and substantive verifier are unchanged. Public certificate and checksum bindings were regenerated and verified. No benchmark was rerun during publication preparation. Original local evidence remains unchanged; replay automation stays paused.
