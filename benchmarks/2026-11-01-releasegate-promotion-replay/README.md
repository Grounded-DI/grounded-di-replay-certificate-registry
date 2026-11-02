# ReleaseGate — seven-boundary synthetic build promotion replay

A fictional release candidate is evaluated against fixed local artifact, provenance, test, approval, destination and policy evidence. Two separate processes generated seven byte-identical canonical artifacts matching independently prepared, frozen expected hashes. A valid candidate produced one synthetic local file; each of 11 negative controls passed its registered assertions. No deployment service was contacted.

## Replay

Use Python 3 and only the standard library. From this directory, in new nonexistent paths:

```sh
sha256sum -c FROZEN_SHA256SUMS.txt
python3 -B pipeline.py --out /tmp/releasegate-A --promote /tmp/releasegate-destination
python3 -B pipeline.py --out /tmp/releasegate-B
python3 -B checker.py --out /tmp/releasegate-A
python3 -B checker.py --out /tmp/releasegate-B
python3 -B -m unittest -v test_releasegate
```

`CONTRACT.json` defines scope and expected control outcomes; `expected_hashes.json` and frozen fixture identities were established before execution. `execution/comparison.json` records hashes and byte equality for all seven files; `run_a/` and `run_b/` preserve the exact outputs. Boundary seven commits to the first six; it is not another independent decision.

`execution/control_results.json` maps the 11 controls to the assertions in `test_releasegate.py`, and `execution/tests.stderr` preserves the raw unittest output: 12 registered and executed, 12 passed, zero failures, errors or skips. Ten rejection tests and the coherent-error control assert that the synthetic destination does not exist, hence the test observes zero writes to that destination. Baseline separately observes one file containing the candidate bytes. The coherent wrong decision also has its manifest digest changed; the release boundary rejects it and the separate checker returns FAIL.

The checker independently recalculates eligibility without importing pipeline code and compares all seven outputs against frozen expected hashes. It shares fixture definitions, the project specification, Python JSON and SHA-256 libraries, and the same machine; it is project-internal, not external verification. Promotion evaluates and checks the candidate locally before a file write; it is not a distributed transaction and does not authenticate the synthetic reviewer or prove real-world provenance, production security, or exactly-once behavior. A host able to alter process state or files is outside the demonstrated boundary.

Raw execution logs contain redacted local workspace paths. The frozen contract and fixtures are unchanged. All inputs and content are fictional. The October 19 Seven-Hash benchmark was not executed or altered.
