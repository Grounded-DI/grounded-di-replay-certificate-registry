# Lighthouse ReleaseGate — seven-boundary promotion replay

A fictional release candidate is evaluated against frozen synthetic policy, provenance, test and approval records. Two fresh Python processes produced seven byte-identical canonical artifacts matching the prewritten expected files and hashes. The final baseline decision was eligible. The seventh artifact commits to boundaries 1–6; it is not an eighth decision or an independent verifier.

[Verification record](verification.json) · [Runnable source and full run package](releasegate_package.zip)

All 11 registered controls executed and passed, with zero failures, errors or skips. Changed artifact bytes, missing provenance, failed or missing tests, missing or mismatched approval, changed destination, changed policy with the same version, and a missing field produced the specified rejection reasons. A downstream alteration failed both decision and commitment checks; a coherently rehashed wrong decision passed commitment verification but failed the separate source-based decision check.

The eligible baseline produced one local promoted file. For rejected cases the promotion function reported zero writes and inspection found no destination files. This is a local synthetic filesystem test, not a real deployment. The declared destination is checked in the request; the caller supplies the physical output directory, which is not bound to that logical destination by this demo.

The project checker separately recalculates the final decision from source records and checks the commitment, but shares the specification, inputs, policy, Python runtime and JSON/hash primitives. It does not recalculate every intermediate artifact. Freeze and execution evidence are local and not independently timestamped. The package makes no external certification, production readiness, exactly-once or universal model-determinism claim.

Package SHA-256: `a06efddaecca527cc8ce494994a4dbaa410eb7a93724cbfe7dcb8fee7ffc3c8e`.
