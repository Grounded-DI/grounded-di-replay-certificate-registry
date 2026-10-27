# Synthetic invoice reconciliation: seven-boundary replay

This finite example demonstrates a batch-local duplicate invoice hold and purchase-order amount limit. The fictional batch pays $86 and holds $76; it is not accounting, purchasing, or fraud advice. See CONTRACT.md for input, rules, expected arithmetic, seven artifact definitions, and frozen checks. All code and input were written for this public synthetic demonstration by Grounded DI's operator. The 2026-10-19 Ulam seven-hash benchmark is a reference, not modified or reproduced here; its archive SHA-256 is recorded in the contract.

From this directory, using Python 3.12.14 and only the standard library, run in new output paths outside the candidate:

```sh
python3 -B demo.py --input input.json --out ../invoice_fresh_a
python3 -B demo.py --input input.json --out ../invoice_fresh_b
python3 -B -m unittest -v test_demo
sha256sum -c SHA256SUMS.txt
```

Compare all seven files in the two fresh output directories directly and against run1 and run2; comparison.json records the original two runs. Receipts contain actual local timestamps outside the byte-identity boundary. test.log records five methods. The altered-output control verifies one changed byte against the original local commitment; it is not a production tamper system. The altered-input test establishes changed arithmetic for one change. The coherent-wrong-result test reissues a self-consistent commitment over a wrong ledger, which passes integrity and fails the hand-stated expected total. The limit test checks equality only. Test logic and manual arithmetic share the stated policy and are project-internal.

The local commitment and checksums are unsigned; matching bytes do not establish correct decisions, external authentication, independent third-party certification, general model determinism, or production readiness. Duplicate checking only covers this batch, in the order supplied. The expected result and all input are synthetic.

SHA256SUMS.txt excludes itself to avoid a self-reference. Verify candidate membership as well as listed checksums. Release verification output is kept outside this candidate to avoid changing the checked file set.
