# Synthetic deadline control — seven-boundary replay

A fictional rule adds ten calendar days to a service date and moves a weekend result to Monday; holidays are excluded. For the synthetic cases A, B and C, the result is 2026-11-16, HOLD, HOLD. This is not a real rule or legal deadline. The frozen rule, cases, boundaries, tests, and commands are in CONTRACT.md.

From this directory, in fresh output directories outside the candidate:

```sh
python3 -B demo.py input.json /tmp/deadline_fresh_1
python3 -B demo.py input.json /tmp/deadline_fresh_2
python3 -B -m unittest -v test_demo
sha256sum -c SHA256SUMS.txt
```

The paths must not already exist. Compare each file in the two fresh directories to run1/ and run2/ directly and by SHA-256. The two original runs, actual local logs, environment and comparisons are included. Stages 01-06 are generated during each computation; stage 07 is an unsigned digest commitment to the first six, generated in each run. A commitment proves consistency with its chosen reference, not correctness or authorship.

Five registered test methods passed. The changed-date test checks one changed output; the missing and ambiguous cases check HOLD; the weekend case tests one Sunday. The changed-output control compares a modified byte string against its original digest. The coherent-wrong-result control constructs a wrong date with a matching replacement digest: this identity check accepts the replacement while the fixed expected-date check rejects it. These are project-local synthetic tests; the latter does not test an external verifier.

Independent arithmetic: 2026-11-06 plus ten calendar days is Monday 2026-11-16. The weekend check starts 2026-11-05, yielding Sunday 2026-11-15, moved to Monday 2026-11-16. Checks share the fictional rule and Python calendar assumptions. No real court holidays, real legal authority, filing, production control, universal determinism, or third-party certification is demonstrated.

SHA256SUMS.txt excludes itself; verify full membership separately. This new demonstrator does not execute a BriefWise runtime. The frozen 2026-10-19 seven-hash benchmark is a methodology reference and was not modified.
