# Fresh Rerun Report: DI² v0.3.1 Local Sidecar Audit

Date: October 21, 2026

## Identity and scope

- Target archive SHA-256: `be0540c28c6a3811012c36f461e32efaec8cf91cc7200b7289917cf4f4710cbf`
- DI² v0.3.1 harness SHA-256: `f45bf63b9ff622b00b697926e8cb941ebbbed763831e088423c4cab8be30c024`
- Pinned public source: `https://github.com/microsoft/ai-agents-for-beginners` at `bb9fd0df2aed2969a403b6d083c34185cad0eb04`
- Frozen case registry SHA-256: `20cf185b705fb5e49f562d1cb794eb4915bde6229e224aa37e5f0cd9e0d7d341`
- Added-control plan SHA-256: `11ef771aefc51c4b340a23bb08f3c01a8b61e5151a466b7bbe57b5656dffe373`
- Execution: local, offline, frozen inputs

## Native lane

**VERIFIED:** 216 PASS, 11 OPA-CLI skips, and 0 failures. Exit status was 0 and the offline network guard was active. This is the canonical result for the selected native replay path.

## Sidecar lane

**VERIFIED:** 80 registered cases completed with 64 PASS assertions and 16 registered Microsoft safety assertions failed. Harness errors: 0. Load errors: 0. Production evidence: false.

**INFERENCE:** The 16 failures group into five public-safe families: mutable approved inputs; incomplete effective argument binding; expiry sampled before the final dispatch boundary; conflicting or duplicate event delivery; and ordered-stage enforcement.

**VERIFIED:** The sidecar's DI² memory and local SQLite paths passed their local control checks where exposed. Added controls passed 9/9. Health mutations were detected 10/10.

## Harness self-replay

**VERIFIED:** DI² v0.3.1 self-replay status was `PASS`. Result comparisons were byte-equal across the fresh rounds; crash recovery status was `PASS`; mutation checks detected 15 of 15 reported mutation outcomes; expiry mutation checks detected 8 with 0 surviving mutations; and source preservation status was `PASS`.

## Public boundary

These are bounded observations in one pinned local implementation. They are not production incidents, live-service findings, model-wide conclusions, whole-product conclusions, or Microsoft vulnerability claims. The package intentionally omits exploit-ready material, private or personal data, hidden prompts, executable source snapshots, payloads, and deployment instructions.
