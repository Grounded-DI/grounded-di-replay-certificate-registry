# DI² Expiry and Policy Replay v1

Source registry: <https://github.com/Grounded-DI/grounded-di-replay-certificate-registry/tree/main/demos/2026-09-10-di2-expiry-policy-v1>

The retrieved ZIP was 28,133 bytes with SHA-256 `b89e8895034223a877d5757495b79463e3d5da9ab300d8320aa4a463b860e8c4`. Fresh processes ran `python3 -B verify.py`, `python3 -B acceptance.py`, and `shasum -a 256 -c SHA256SUMS.txt`; all exited 0. The evidence covers 25 recorded cases, 10 boundary checks, six altered-copy controls, expiry and policy-hash behavior, reference agreement, replay identity, real-clock expiry, and unchanged original files.

See the [full report](replay_report.md) and [complete reproducibility archive](DI2_Expiry_Policy_Replay_v1_reproducibility_package_v2.tar.gz).

This is a local synthetic authorization harness. It is not an installed application enforcement feature or external security certification.
