# VerdictBridge Demo 3 Fresh Replay — Lane Report

Selected registry path: `demos/2026-10-07-verdictbridge-demo3-fresh-replay`.
Source: https://github.com/Grounded-DI/grounded-di-replay-certificate-registry/tree/main/demos/2026-10-07-verdictbridge-demo3-fresh-replay

This lane replayed the published fresh-replay package; no excluded demo was rerun. The original ZIP was preserved unchanged at `source/VerdictBridge_Demo3_Fresh_Replay_Public_v1.zip`.

Archive SHA-256: `8f401a26711b423055079423e766558e1b2ec82309bbc470d469969d5bd448cc`. Retrieval metadata: `retrieval_start.txt`, `contents.json`, `package.json`. Environment and file hashes: `environment_and_hashes.txt`.

Commands run in fresh processes: `python3 -B package_run/verify_package.py`, `python3 -B package_run/replay/source/verify.py`, `python3 -B package_run/replay/source/acceptance.py`, and `python3 independent_calc.py`; all exited 0. Raw stdout/stderr are preserved in the corresponding files.

`independent_calc.py` parses canonical input directly and applies separately written predicates; it does not import or call verifier logic. Complete trace: `independent_trace.json`. Result: strict liability, negligence, and compensatory damages deny summary judgment; punitive damages grant summary judgment; overall granted in part/denied in part; Sam Reed excluded; jury coverage PASS; VerdictReady YES; export authorized true.

| Check | Result | Evidence |
|---|---|---|
| Package manifest/certificate integrity | PASS | `verifier_stdout.txt`; 127 manifest entries, 126 certificate bindings |
| Packaged replay verifier | PASS | `replay_verify_stdout.txt` |
| Acceptance/tamper controls | PASS | `acceptance_stdout.txt`; seven controls rejected |
| Three-run five-artifact hash match | PASS | `package_run/verification/measured-results.json` |
| Direct byte comparison | PASS | measured-results; zero mismatches |
| Invalid hearsay refusal/export boundary | PASS | VerdictReady NO, authorization false, zero opens/writes |
| Independent calculation agreement | PASS | `independent_trace.json` |
| External certification/original-engine execution | UNRESOLVED | outside scope |

Limitations: finite synthetic replay only. Original engine execution, external certification, universal model determinism, legal compliance, and independent fresh-generation provenance are not established.

Evidence archive: `vb_fresh_reproducibility_package.tar.gz`.
