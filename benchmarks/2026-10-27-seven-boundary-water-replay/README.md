# Synthetic Water Allocation: Seven-Stage Replay

Grounded DI LLC · October 27, 2026. This is a new, finite demonstration inspired by the [frozen seven-hash benchmark](../2026-10-19-seven-hash-replay-closure/README.md); it does not modify or replay that benchmark. All sites, quantities, and priorities are fictional. This is not emergency response guidance.

A supply of 1,100 liters includes a protected 100-liter reserve. The remaining 1,000 liters are allocated in fixed priority order: clinic receives 500 of 500 liters, shelter 500 of 700, and warehouse 0 of 200. Total unmet demand is 400 liters. The algorithm is a simple declared policy, not an optimized or expert allocation.

## Seven boundaries

The following are distinct generated stages, each compared by direct bytes and SHA-256 across two fresh Python processes: normalized input (`01_input.json`), usable budget, ordered plan, allocation ledger, unmet-demand ledger, balance record, and final disposition. These are fresh computations of a newly written evaluator, not seven independently implemented systems. No packaging identity is claimed. The frozen contract, literal expected outputs, and comparison rules appear in `CONTRACT.md` and `test_demo.py`.

## Reproduce

Use Python 3 standard library on a POSIX host; this run used Python 3.12.14 on Linux. From this directory:

```sh
python3 -B demo.py --input input.json --out /tmp/water-replay-a
python3 -B demo.py --input input.json --out /tmp/water-replay-b
python3 -B test_demo.py
sha256sum -c SHA256SUMS.txt
```

Use new output directories. The stored `run1/` and `run2/` contain the generated artifacts, and `run1.json` and `run2.json` are their process outputs. The test suite verifies a separate pair of fresh runs and compares the substantive results to independently hand-calculated literals; it shares the same Python runtime and test specification. `test.log` records seven test methods, including the expected detection of altered input/output, zero-budget and exact-demand boundaries, and five invalid-input variations. Mutation checks compare altered bytes or outputs; they do not establish a production tamper-detection service. `SHA256SUMS.txt` covers every delivered file except itself.

## Scope and limits

The two computations ran on one host with the same code and environment. The literal arithmetic is a separate check, not an independent software implementation or external certification. No model endpoint, live provider, real operating environment, or original benchmark computation was run. Hash equality demonstrates byte identity for these files under this contract, not the soundness of the allocation policy or universal determinism. Local receipts are unsigned.
