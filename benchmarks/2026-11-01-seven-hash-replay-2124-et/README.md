# Seven-Hash replay — November 1, 2026, 9:23 p.m. Eastern

Two fresh local computational builds matched the six frozen boundaries. Two separate packaging processes reproduced the original 116-member historical delivery ZIP byte-for-byte. All seven boundaries matched their retained expected values. The seventh is a reconstruction of the same frozen payload, not a new computational build.

[Machine-readable verification](verification.json) · [October 19 closure](../2026-10-19-seven-hash-replay-closure/README.md) · [Earlier November 1 replay](../2026-11-01-seven-hash-fresh-replay/README.md)

All eight comparison files from both new builds were directly byte-compared against each other and the retained baseline. The separate project mathematical verifier passed 49 checks on each fresh build; the original A and B verifications passed. The unit suite ran 31 tests with no failures, errors or skips; all 14 negative controls passed. All eight recorded command categories exited zero.

The original ZIP, unsigned detached receipt and frozen contract matched the identities in verification.json. The run used Python 3.12.14, NumPy 2.3.5, Pillow 12.3.0 and zlib 1.3.2. The historical record lists Python 3.13.5 and zlib 1.3.1; the frozen contract binds that record but does not prescribe those versions for this execution. The separately identified October 19 strict-replay and closure evidence archives were not obtained in this run and are not required by the frozen execution contract or this mission.

The private supplemental evidence archive is retained outside this repository, SHA-256 `6bf521217606f3176a111421661ce5ef623d6df8e4517ddfbbbea90796c587ab`. It retains the run records and omits two packaging ZIP copies recorded as byte-identical to the separately retained original. Those reconstructed ZIP bytes are not independently retained in the supplement. The full local archive could not be saved due to a storage limit; this did not change the replay result.

This is a project-executed local replay. The mathematical verifier uses a separate implementation on the same host and shares standard-library primitives. It is not independent external certification, proof of universal model determinism, or a cross-platform reproducibility claim. The historical benchmark and prior records remain unchanged.
