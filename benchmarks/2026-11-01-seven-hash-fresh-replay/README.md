# Seven-Hash Benchmark — Fresh Local Replay, November 1, 2026

Two fresh computational builds reproduced the six frozen computational boundaries, and two separate packaging processes reproduced the original historical delivery ZIP. **All seven boundaries matched their expected values.** The two packaging processes used the same unchanged 116-member historical payload; they were not new computational builds.

[Machine-readable verification](verification.json) · [Technical record](REPORT.md) · [Checksums](SHA256SUMS.txt) · [October 19 closure](../2026-10-19-seven-hash-replay-closure/README.md)

The two fresh builds each passed 49 checks in the separately implemented project mathematical verifier; the original bundled A and B records each passed 48 current verifier checks. The 31-test unit suite and all 14 negative controls passed. All eight compared build output files matched the retained baseline and each other byte for byte. The negative controls include a self-consistent mathematical error that integrity checks alone do not reject.

The original benchmark and its unsigned detached receipt were verified. The separate October 19 strict-replay and closure-recheck evidence ZIPs were not located in this cycle. The new raw evidence archive is retained separately and is not hosted in this repository.

The current runtime was Python 3.12.14 and zlib 1.3.2; the original environment record lists Python 3.13.5 and zlib 1.3.1. NumPy 2.3.5 and Pillow 12.3.0 matched the recorded versions. The frozen contract binds the historical environment record but does not require those exact runtime versions. The actual outputs matched under this observed environment; broader cross-platform reproducibility is not established.

This is a local, self-recorded replay and is not external certification or a claim about universal model determinism. The original reference and closure remain unchanged.
