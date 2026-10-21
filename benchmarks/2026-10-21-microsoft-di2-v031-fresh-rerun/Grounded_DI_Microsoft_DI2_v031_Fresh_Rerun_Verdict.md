# Fresh Rerun Verdict

## Result

**VERIFIED:** The canonical native replay completed with 216 PASS, 11 OPA-CLI skips, and 0 failures.

**VERIFIED:** The DI² v0.3.1 sidecar completed 80 registered cases with 64 PASS and 16 registered Microsoft safety assertions failed; 0 harness errors and 0 load errors.

**VERIFIED:** The DI² v0.3.1 self-replay passed local integrity, repeatability, mutation, expiry, receipt, and crash-recovery checks.

## Classification

`LOCAL SYNTHETIC HARDENING CANDIDATE; OPTIONAL PERSISTENT LOCAL GATE`

## Interpretation

The native and sidecar lanes remain separate. The sidecar failures are bounded local control-gap observations grouped into five conceptual families. They do not establish a production incident, live-service behavior, exploitability, severity, Microsoft knowledge or endorsement, or whole-product behavior.

## Release posture

Production readiness is **UNESTABLISHED**. This package is public-safe evidence for a pinned local replay and a local hardening candidate only.
