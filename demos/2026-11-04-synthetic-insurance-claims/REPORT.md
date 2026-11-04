# Claims replay — 4 November 2026

## Outcome
Synthetic fictional equipment-water claims; six records. Two route for synthetic payment, three hold, one denies. Counts refer only to this ruleset. Frozen/EXPECTED.md provides the separate pre-implementation manual arithmetic. SPEC.md and fixture were created before producer/checker implementation; TEST_PLAN.md was frozen after the first baseline run and before adversarial testing. No timestamps or hashes establish third-party timestamping.

## Execution and results
From the directory containing this package (Python 3.11+, standard library):

    python3 -B src/producer.py frozen/fixture.json /tmp/claims-run-a
    python3 -B src/producer.py frozen/fixture.json /tmp/claims-run-b
    python3 -B src/checker.py frozen/fixture.json /tmp/claims-run-a
    python3 -B src/checker.py frozen/fixture.json /tmp/claims-run-b
    python3 -B src/test_replay.py

Use fresh output paths. The test runner uses the included evidence/run1 and run2 as its frozen baseline and creates mutation runs in a new temporary directory. Running it writes a new evidence/test_results.json; make a copy first to preserve this archived result. Runtime environment and each case's expected/actual, exit, reason/status, and directory before/after are in evidence/test_results.json. The first baseline producer/checker commands exited 0 with OK. Seven artifact byte comparisons matched; corresponding SHA-256 values are in test_results.json. Checker accepted both. The registered test runner has 53 passed, 0 failed, 0 errors, 0 skips; its cases include seven comparisons, two checks, one expected-decision comparison, 24 malformed-input producer/checker cases, 11 changed-scenario cases, five artifact corruptions, a post-generation input mutation, an existing-destination replay, and a serialization case. The runner itself has no exception recovery: an unexpected crash would terminate the suite rather than be counted as a case error. Its reported zero errors means this completed run had no runner exception, not a separate per-case error framework.

The input mutation and artifact mutations produced CHECK_FAILED/1. A decision/disposition forgery with recalculated commitment was rejected against the frozen input. Existing destination was preserved and returned OUTPUT_EXISTS/2. New valid policy versions were accepted and recomputed, as designed; they were not treated as authenticated or unauthorized. Input/outputs are local files, not authoritative external records. Output directory creation and writes are not atomic, and I/O failures can leave a partial newly created directory. Concurrent creation and exactly-once effects are outside scope. Extra unlisted files in an output directory are ignored by the checker. Duplicate evidence takes precedence over evidence binding/conflict in this demonstration. Full schema/validation details appear in the spec and source.

## Implementation and independence
Producer and checker are separate source files and processes, do not import each other, and each calculates the decision and all artifact bytes. They share the Python standard library, the same explicit schema, rules, SHA-256 and JSON serialization design; shared interpretation bugs are possible. The checker accepts the supplied input as truth and checks expected bytes, including the commitment. It does not authenticate a policy, verify evidence against an external system, or detect a coherent substitution of both the trusted input and generated output. The hash commitment does not establish truth or authorship. Hand calculations cover final baseline outcomes; they are not an independent external review.

## Harness use
The separately supplied Everyday Harness v0.3.1 quickstart was run earlier in this session. Its package integrity before/after, native core, and native unit commands exited 0; the private session receipt and logs are not included in this public copy. The harness was not linked to, and did not enforce or evaluate, this insurance producer/checker. Its bundled README distinguishes six deliberately defective fixture assertions from passing safety properties. This demonstration uses its own code and tests. No complete Tier or product conformance is claimed.

## Limits
Fictional policy only; not legal, insurance, claims-handling, regulatory or production validation. No identity, source provenance, external trust anchor, secrets, database, real system integration, denial delivery, or payment. Spec and test plan are local records and are not signed. Avoid treating deterministic replay as proof of correctness for other policies or as proof that a source record is authentic.
