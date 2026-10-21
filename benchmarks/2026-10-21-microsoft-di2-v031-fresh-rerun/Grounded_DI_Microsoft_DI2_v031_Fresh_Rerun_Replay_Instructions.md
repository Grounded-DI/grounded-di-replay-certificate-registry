# Fresh Rerun Replay Boundaries

Use only the exact locally preserved inputs for a new reproduction.

## Required identities

- Target archive SHA-256: `be0540c28c6a3811012c36f461e32efaec8cf91cc7200b7289917cf4f4710cbf`
- DI² v0.3.1 harness SHA-256: `f45bf63b9ff622b00b697926e8cb941ebbbed763831e088423c4cab8be30c024`
- Pinned public source commit: `bb9fd0df2aed2969a403b6d083c34185cad0eb04` at `https://github.com/microsoft/ai-agents-for-beginners`
- Frozen case registry SHA-256: `20cf185b705fb5e49f562d1cb794eb4915bde6229e224aa37e5f0cd9e0d7d341`
- Added-control plan SHA-256: `11ef771aefc51c4b340a23bb08f3c01a8b61e5151a466b7bbe57b5656dffe373`

## Safe sequence

1. Verify every identity before execution. Stop on any mismatch or missing harness.
2. Run the target package's native replay in a local offline environment and preserve its native summary separately.
3. Run the same frozen inputs through DI² v0.3.1 and the relevant local adapter or boundary. Preserve sidecar summaries separately.
4. Run the candidate self-replay and record integrity, repeatability, mutation, expiry, receipt, and crash-recovery results.
5. Compare lanes without merging scores. If they differ, preserve both outcomes and record the smallest non-operational counterexample.

## Boundaries

Do not connect to live services, alter the target, alter the harness, replace the frozen inputs, substitute a different harness version, publish raw source snapshots, or include payloads or attack recipes. A skipped or unsupported case is not a pass. The reproduction can establish only the tested local path and its recorded configuration.

## Expected fresh-run shape

- Native: 216 PASS, 11 OPA-CLI skips, 0 failures.
- Sidecar: 64 PASS, 16 registered Microsoft safety assertions failed, 0 harness/load errors.
- Candidate self-replay: PASS; local synthetic hardening classification.

These expected values are a record of this fresh run, not a promise that an independently configured environment will match them.
