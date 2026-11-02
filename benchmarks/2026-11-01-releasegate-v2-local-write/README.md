# ReleaseGate V2 — actual local destination binding

Two fresh local processes matched all seven frozen expected artifacts byte for byte and by SHA-256. The eligible baseline wrote one synthetic candidate to the authorized relative path. Each of 12 registered controls passed, with zero failures, errors or skips. Rejected tests reported zero writes and found no files at either the authorized or attempted destination.

[Verification](verification.json) · [Reproducibility package](ReleaseGate_V2_Reproducibility.zip) · [Clean extraction recheck evidence](ReleaseGate_V2_Extraction_Recheck.zip)

Controls covered changed bytes, missing provenance or tests, changed or missing approval, changed declared or physical destination, traversal, same-label policy mutation, missing required field, and rehashed tampering with an intermediate artifact or final decision. A separate project checker recalculates boundaries 1–6 from source records and verifies boundary 7; boundary 7 is a commitment, not an independent verifier.

The actual write is restricted to a fixed relative path under a trusted, precreated local sandbox. The test assumes the sandbox and parent are not concurrently changed; it does not establish security against hostile processes, symlink or mount races, or crashes. The producer and checker share the project, contract, policy, host, Python, JSON and hash primitives. Inputs and evidence are synthetic and unsigned. This is not external certification, production readiness, a real deployment, exactly-once delivery, or a universal model-determinism claim.

The included package was extracted into a clean directory and its documented suite passed again; that recheck evidence is separate to avoid self-reference. Freeze timing is a locally recorded execution sequence, not independently timestamped.
