# VerdictBridge Demo 3 Published Replay — lane report

## Selection and source

Selected as an eligible complete replay at `demos/2026-10-08-verdictbridge-demo3-published-replay` in the Grounded DI replay registry, after excluding previously completed lanes. Registry source: https://github.com/Grounded-DI/grounded-di-replay-certificate-registry/tree/main/demos/2026-10-08-verdictbridge-demo3-published-replay

Retrieved `README.md`, `VerdictBridge_Demo3_Published_Replay_Public_v1.zip`, its `.sha256` file, and the complete package support files directly from the registry raw URLs. Retrieval metadata is in `retrieval.json`. ZIP size was 873,102 bytes and SHA-256 was `6e5399378479d8e7dc030f6c9139b93449978fd5cf57b39c5055e8eb4f05c5a6`, matching the registry checksum.

## Environment and execution

Linux x86_64 (kernel 6.18.55), CPython 3.12.14. Working directory: `/workspace/scratch/cfd2224648bf/four_lane_replay/vb_published`. The archive was extracted to `package_extracted2/` without modifying its contents. A separate verifier workspace was used so the downloaded package remained unchanged.

Commands executed include:

```sh
unzip -q downloads/VerdictBridge_Demo3_Published_Replay_Public_v1.zip -d package_extracted2
(cd verifier_workspace && python3 -B verify_package.py)
(cd package_extracted2/VerdictBridge_Demo3_Published_Replay_Public_v1/replay/source && python3 -B verify.py)
(cd package_extracted2/VerdictBridge_Demo3_Published_Replay_Public_v1/replay/Run-A && python3 -B ../source/acceptance.py)
python3 independent_calc.py
```

Raw stdout, stderr, exit codes, and timestamps are preserved in `evidence/`.

## Independent calculation

`evidence/independent_calc.py` is separate from the packaged verifier. It reconstructs the expected disposition from the preserved canonical result fields, checks all predicate flags, compares all five canonical artifacts byte-for-byte across Run-A/Run-B/Run-C, validates the refusal boundary, verifies the manifest and ZIP CRC, and records a complete JSON trace in `independent_calculation_trace.json`.

Observed disposition: strict-liability failure-to-warn, negligence, and compensatory damages `DENY_SUMMARY_JUDGMENT`; punitive damages `GRANT_SUMMARY_JUDGMENT`; overall `GRANTED_IN_PART_DENIED_IN_PART`; Sam Reed `EXCLUDED_AND_NOT_USED`; VerdictReady `YES`; export authorized `true`. The hearsay control was refused with VerdictReady `NO`, authorization `false`, zero files opened, and zero bytes written. All seven recorded tamper controls were rejected.

## Check table

| Check | Result | Evidence |
|---|---|---|
| Source ZIP hash and byte length | PASS | `retrieval.json`, `.sha256`; 873102 bytes; SHA-256 above |
| Package manifest and certificate integrity | PASS | `evidence/verifier.stdout`; 202 manifest entries, 201 bindings |
| Packaged semantic verifier | PASS | `evidence/semantic.stdout`; exit 0 |
| Packaged acceptance controls | PASS | `evidence/acceptance.stdout`; exit 0 |
| Independent disposition reconstruction | PASS | `evidence/independent_calc.stdout` |
| Predicate checks | PASS | independent trace; all ten true |
| Three-run canonical artifacts byte-identical | PASS | independent trace; five artifacts, zero mismatches |
| Hearsay refusal and zero-write boundary | PASS | independent trace and preserved invalid-control files |
| Seven tamper controls rejected | PASS | `execution/acceptance-controls.stdout.txt` |
| SHA-256 manifest | PASS | independent trace |
| ZIP CRC | PASS | independent trace (`testzip() is None`) |
| Package unchanged after verification | PASS | `evidence/package_hashes_after.json`; verifier workspace was separate |

## Limitations

This is a bounded synthetic replay of the published Demo 3 package. It is not original-engine execution, unaffiliated validation, external certification, or legal compliance evidence. Matching canonical bytes do not establish independent fresh-generation provenance. Results do not generalize to real legal decisions or litigation outcomes. The registry itself records that the published executable path was redacted and unrecorded machine state is not established.

## Reproducibility package

The lane package preserves downloads, extracted package, verifier workspace, raw process evidence, environment, commands, independent calculation code/trace, and this report.
