# Seven-Hash Replay — Independent Local Run, November 1, 2026

Two fresh computational builds matched all six frozen computational boundaries and all eight reference output files directly byte for byte. Separately, two packaging processes reconstructed the unchanged historical 116-member payload; each matched the original ZIP directly byte for byte. This packaging was not a fresh computational build or new evidence package.

[Machine-readable verification](verification.json) · [October 19 closure](../2026-10-19-seven-hash-replay-closure/README.md) · [Prior November 1 record](../2026-11-01-seven-hash-fresh-replay/README.md)

The project-local mathematical verifier passed 49 checks per fresh build and 48 per original reference run. The unit suite registered and executed 31 tests with no failures, errors or skips; all 14 registered negative controls executed and passed. The verifier uses independently implemented mathematical algorithms but shares the project, host, specification and Python standard-library primitives. The unsigned detached receipt and 116-member inventory were verified.

Python 3.12.14 and zlib 1.3.2 differed from the recorded historical Python 3.13.5 and zlib 1.3.1. The frozen contract binds the environment record but does not expressly require those versions. NumPy 2.3.5 and Pillow 12.3.0 matched the recorded versions. The separate October 19 strict-replay and closure-recheck archives were not located in the preceding cycle; the frozen contract and this mission do not expressly require them.

This is local, project-executed evidence; it is not external certification, a cross-platform claim, or universal model determinism. The current raw evidence archive is privately retained and is not hosted in this repository; its SHA-256 is `e41afa9aa3d26a1710c40fe7b8fcc108eca429ca0b3f84766330f25132286b0c`.
