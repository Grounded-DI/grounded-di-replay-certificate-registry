# Seven-Hash Replay Benchmark — Final Local Closure (October 19, 2026)

**Disposition:** PASS — local, qualified runtime. **Development status:** frozen regression reference; no further benchmark expansion planned at publication.

## What was verified

The frozen Grounded DI Seven-Hash Replay Benchmark v1 was checked against its detached, unsigned local SHA-256 receipt. Two previously executed fresh computational builds independently matched the reference at six boundaries: CSV, NPZ, PNG, manifest, prime mask, and Merkle root. In the final recheck, an independent mathematical verifier was rerun against both builds (49 checks per build). The original unit suite passed 31/31, and the negative-control suite passed 14/14.

Boundary seven is **not** a newly generated evidence ZIP. Two separate canonical packaging processes reconstructed the **unchanged frozen 116-member historical payload**, with both resulting ZIPs matching the original delivery ZIP byte-for-byte.

**Frozen historical delivery ZIP SHA-256:** `497614c00216d7fe86886afdfd93aa7c08a5d65a590c38dd8a78e5380d80fa98`

## Negative observation preserved

The first final-recheck packaging attempt inadvertently included seven Python `__pycache__` entries, yielding 123 members instead of 116 and a mismatched hash. A new clean extraction, packaged **before** running tests and with tests executed on a separate copy, produced two exact-byte matches. The failed attempt and the corrective recheck remain in the local evidence archive. This is a source-directory contamination failure, not a prime-mathematics discrepancy.

## Artifact identity and access

- Frozen reference: `GroundedDI_SevenHash_ReplayBenchmark_v1_20261019.zip` — 13,245,692 bytes, SHA-256 above.
- Strict replay evidence: `GroundedDI_SevenHash_StrictReplay_Evidence_20261019_231501_UTC.zip` — SHA-256 `ac5a4992b35891898f396d0d852236b87eda3a949a251e7837ea0de633eef348`.
- Final fresh-recheck evidence: `GroundedDI_SevenHash_Closure_FreshRecheck_20261019.zip` — SHA-256 `3b2d179a1c3374218093cc2d94e343a397ebcecdf3847e208d4f55f3dd3f6f32`.

**Publication scope:** This record publishes the result and artifact identifiers. The binary evidence archives are **not uploaded by this commit** and must not be described as downloadable from this repository until separately attached and checksum-verified.

## Interpretation

The evidence demonstrates reproducible computation and canonical repackaging in a compatible local environment, together with independent domain checks and finite negative controls. It does **not** establish external certification, cross-platform reproducibility, universal model determinism, or a new theorem about prime numbers.

The benchmark is frozen for regression use. Future engineering work should focus on applying these controls to practical Grounded DI systems.
