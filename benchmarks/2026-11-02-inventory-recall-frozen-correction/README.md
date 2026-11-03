# Inventory-to-recall synthetic replay: frozen correction

**PASS — local project-executed replay.** Two fresh processes matched seven retained expected artifacts byte for byte and by SHA-256. Both checker runs and nine controls passed; a clean extraction repeated the checks. The evidence package is retained privately (SHA-256 `47f78033a3d5667df5a4ace2dd25564747fc06f0c5711b7f4881d8e39abf1e40`); it is not hosted here.

A fictional receipt precedes an applicable lot recall. Under the fixture's policy, the later release is held while the prior receipt remains recorded. Five requests produce: permit 7, hold 0 for recall, hold 0 for missing lot identity, partial 4 for insufficient stock, and permit 6 where a notice names another lot. No physical distribution occurs.

## Evidence

| Artifact | Expected and observed SHA-256 | Byte comparison |
| --- | --- | --- |
| 01.json | `fa170302106444fbd8a78b8a30d7681c2d45520a0e0abebc5adb9da3b2033b5e` | match |
| 02.json | `3285f6aa7426ac4b305e401e6b07dc004caef3b8fae6d7f90f225cdde52e79ff` | match |
| 03.json | `3c8ba3a3bca08533d9c784e4cd7a10fc97e9c6e931d87887ae32ab1e683abf0a` | match |
| 04.json | `86ff80b295a1deca15a21e6b4ab23779bff237886803a2ab522c2ec6b8dd6cb0` | match |
| 05.json | `f7562126cc42bf7e6157436e67ef5fae884754f85c59ab34307ae4ad297fbb23` | match |
| 06.json | `83502ab4f5ad39cfb07e000606d19e4be0f036bf751afd76b83a9bbb1fd2895c` | match |
| 07.json | `c3a738580433cb5c31474a461da52a02934daf8a46cf140407afe511828b3d4d` | match |

The corrected-source manifest was created before the new run at 2026-11-03 03:59:12 UTC; its SHA-256 is `eced1cbdca67c8cfc9cfb02453f2c54842335ba9c7cf807604df526d7a516ff9`. Checks passed before and after execution. Boundary 7 commits to the first six and is not an independent verifier.

Nine controls were registered, executed and passed, with zero failures, errors or skips. They cover changed identity, applicable and unrelated notices, recall timing, missing receipt and unit, insufficient stock, tampering with an intermediate record, and a coherently rehashed wrong final decision. Each control was also executed individually with process exit code zero.

## Failure history

The initial checker failed to start due to a missing parenthesis; its controls did not execute. A second attempt corrected the checker and passed the recorded tests, but did not freeze a corrected-source checksum manifest before execution; publication was halted. This third attempt retained the original contract, fixture and expected bytes, used the corrected source and froze a new manifest before execution.

The available warehouse-recall draft describes shared-stock allocation across prioritized orders; this scenario focuses on the timing of a notice between receipt and proposed release. The checker is separately implemented but shares the specification, fixture, serialization, Python libraries and host with the producer. This local synthetic example does not establish actual recall protection, physical delivery, external certification, production readiness or universal model determinism.
