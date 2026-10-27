# Synthetic cold-chain inspection: seven-boundary replay

This self-contained example uses fictional temperature readings and a fictional policy to decide whether a shipment receives RELEASE or HOLD. A +0.2°C calibration adjustment yields 4.0, 7.8, 8.1 and 5.0°C. With a made-up 2.0–8.0°C inclusive range, one reading triggers HOLD; all gaps and coverage pass. This is not clinical, regulatory, product-quality or shipment advice. The rule checks only measured samples, not temperatures between them.

CONTRACT.md records the input, assumptions, seven generated boundaries, expected arithmetic and test plan. Boundaries 01–06 are stage records; 07 commits to their hashes. Two separate processes running the same code on one host generated matching files; comparison.json records both SHA-256 values and direct-byte checks. run1_receipt.json and run2_receipt.json preserve process metadata outside the matching-byte records.

From this directory, with Python 3.12.14 on Linux and no third-party dependencies, run with new output directories:

```sh
python3 -B demo.py --input input.json --out ../cold_fresh_a
python3 -B demo.py --input input.json --out ../cold_fresh_b
python3 -B -m unittest -v test_demo
sha256sum -c SHA256SUMS.txt
```

Compare the seven files across both fresh outputs and preserved runs. The manifest excludes itself; separately check the complete file membership. test.log records all eight methods. The changed-output control checks one modified decision against the local commitment; the coherent-wrong-result control rebuilds the commitment around a false RELEASE and passes integrity while the fixed expected result detects the discrepancy. This is an internal demonstration, not a production tamper service. Manual calculation shares the synthetic policy and is not an external certification.

The frozen 2026-10-19 Grounded DI Ulam seven-hash benchmark is methodology background, not changed or rerun here. The source and inputs in this new demonstration were created for the mission and are offered as a public example by the operator. Local receipts and the commitment are unsigned. Hash matches show artifact identity under the contract, not correctness, universal model determinism, live system enforcement, or production readiness.
