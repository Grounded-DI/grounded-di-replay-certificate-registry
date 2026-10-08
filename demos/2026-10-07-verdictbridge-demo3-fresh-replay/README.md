# VerdictBridge Demo 3 - fresh replay, October 7, 2026

**PASS within the stated finite scope. Internal verification; unaffiliated review pending.** This is a fresh replay of the existing closed-world Demo 3 benchmark, not a new benchmark.

[Two-page PDF](package/Fresh_Replay_Report.pdf) · [Complete public ZIP](VerdictBridge_Demo3_Fresh_Replay_Public_v1.zip) · [ZIP checksum](VerdictBridge_Demo3_Fresh_Replay_Public_v1.zip.sha256) · [Runnable package and instructions](package/README.md)

Three fresh evaluator processes produced five canonical artifact types byte-identical across all three runs and against the pinned historical artifacts. The declared selective legal result passed the separate internal verifier. The inadmissible-hearsay candidate was refused with VerdictReady NO, export authorization false, zero export-file opens, zero bytes written and an empty inventory. All seven prescribed tamper controls were rejected.

Exactly the same declared output under the same frozen execution conditions, with receipts showing what actually ran, SHA-256 hashes, and direct byte comparisons. Material changes produce a specified changed result or refusal.

That framing is limited to the conditions and controls actually tested. Canonical ZIP metadata uses January 1, 1980. Real process IDs and execution timestamps remain in separate receipts. Those receipt fields changed; canonical bytes did not. Historical OS/interpreter identity remains UNKNOWN. The complete public ZIP has different contents and a distinct hash.

## Evidence

- [Measured results](package/verification/measured-results.json) and [all fifteen hashes](package/HASHES.md)
- [Fresh run folders, unchanged source and case specification](package/replay/)
- [Invalid control](package/replay/invalid-hearsay-control/) and [acceptance results](package/execution/acceptance-controls.stdout.txt)
- [Environment](package/environment.json), [execution commands](package/execution/commands.json), [certificate](package/replay-certificate.json), [manifest](package/SHA256SUMS.txt)
- [Public packaging/redaction record](package/PUBLIC-RELEASE-NOTES.json)

Original preserved references, the previously implemented local evaluator, its separate internal verifier, and measured executions are distinct evidence layers. No original-engine execution, native VerdictBridge reproduction, universal generative-model determinism, external certification or legal compliance is claimed. The PDF is an unchanged execution-time report; its local/unsent wording describes the earlier preparation state.

Source evidence pin: `ac3a8cd522718235d2a7154c728566614086a809`. Public ZIP SHA-256:

```text
8f401a26711b423055079423e766558e1b2ec82309bbc470d469969d5bd448cc
```

The public derivative removes machine-specific paths from logs and omits the local controller and unrelated preservation inventory. Canonical artifacts, receipts, source/specification/reference files and PDF are unchanged. New public manifest/certificate bindings were verified. No new benchmark run occurred during publication preparation. The private local evidence and reviewer handoff remain unchanged. Replay automation remains paused.
