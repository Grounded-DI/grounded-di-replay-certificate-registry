# FlightGate Demo 008

Source registry: <https://github.com/Grounded-DI/grounded-di-replay-certificate-registry>

The four retrieved ZIP copies were each 67,577 bytes with SHA-256 `3fa71e81d75cceb52f2b6d12bd45983e1253113bba7ee112b75161a5397a9496`. The two fresh verifier commands used `06_verify_demo.py` with ZIP pairs 1/2 and 3/4. Both verifiers exited 0. Independent calculation reproduced FLY=4 and NO_FLY=6, exact-boundary behavior, the 25-to-24 wind-limit mutation, fail-closed configuration probes, and the synthetic five-blocker auditor probe. Manifest, CRC, byte-identity, stdout-identity, and package-preservation checks passed.

See the [full report](replay_report.md) and [complete reproducibility archive](FlightGate_Demo008_reproducibility_package_v2.tar.gz).

This is a synthetic rule-execution demonstration and does not authorize or generalize to real flight operations or aviation safety.
