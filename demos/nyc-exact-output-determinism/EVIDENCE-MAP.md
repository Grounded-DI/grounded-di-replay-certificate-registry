# NYC Evidence Map

This map connects the five NYC reviewer questions to existing public registry evidence. The artifacts remain in their existing locations and are not duplicated here.

| NYC question | Evidence instance | Domain | Replay evidence | Controlled change/refusal | Boundary result | Provenance commit | Classification |
|---|---|---|---|---|---|---|---|
| 01 — Exact input / exact output | [VerdictBridge Demo 3](../2026-10-05-verdictbridge-punitive-control-v1/README.md) | Legal workflow | Three distinct evaluator processes from the same frozen input; five artifact comparisons; direct byte and SHA-256 agreement | Invalid-hearsay and altered-copy controls are rejected | Zero export opens, zero bytes written, empty invalid-control inventory | `90b0b0cbe5eb244412b2c6befab273a137c51c3a`; original reference `8472b48470b6c35a3ad2778f0819f36d4ddaef1b` | REUSE AS-IS |
| 02 — Material input / controlled output change | [ChainGate Demo 10](../../10_ChainGate_Demo_Record.txt) | Logistics | Fresh verifier executions; two delivered ZIP archives are byte-identical and manifest-checked | Maximum temperature 8.0 produces RELEASE; 7.9 produces HOLD | Explicit RELEASE/HOLD routing with triggered-rule reporting | Current-tree pin `90b0b0cbe5eb244412b2c6befab273a137c51c3a`; historical record commit `33ce180aacee6503f6f3994fc643cb9f77507752` | REPACKAGE / INDEX |
| 03 — Invalid or disallowed input / refusal | [Expiry and Policy Replay](../2026-09-10-di2-expiry-policy-v1/README.md) | Authorization/export | Fresh evaluator processes reproduce canonical replay identity and saved exports | Expiry, policy changes, malformed evidence, altered artifacts, and destination changes are rejected | Denied cases reach no export-open branch | `3286b58800c4d97519b707fa8df5b4348d9a61a8` | REUSE AS-IS |
| 04 — Cross-domain replay | [FlightGate Demo 08](../../08_FlightGate_Demo_Record.txt) | Aviation-style synthetic routing | Separate verifier executions; four delivered ZIP archives are byte-identical | Threshold 25 produces FLY; threshold 24 produces NO_FLY; unknown configuration is rejected | FLY/NO_FLY routing and fail-closed missing-field handling | Current-tree pin `90b0b0cbe5eb244412b2c6befab273a137c51c3a`; historical record commit `33ce180aacee6503f6f3994fc643cb9f77507752` | REPACKAGE / INDEX |
| 05 — Scope / revalidation boundary | [Global Multirow Coercivity](../../02_Global_Multirow_Coercivity_Master_Certificate_Intake_Record_v2.txt) | Exact mathematics | Clean-room verifier replayed the corrected source-functional packet and certificate | Original release rejected for a packaging/self-containment defect; corrected release accepted without changing mathematical artifacts | Packaging and source-function boundary requires revalidation before acceptance | Attestation materials `4cfc13219edb4f694705827a02bed0b25932662c`; current-tree pin `90b0b0cbe5eb244412b2c6befab273a137c51c3a` | REPACKAGE / INDEX |

## Supporting-artifact classification

| Existing artifact family | Classification | Role in the NYC index |
|---|---|---|
| Replayable Authorization | REUSE AS-IS | Supporting action/destination binding and pre-write refusal |
| Single-Use and Crash Recovery | REUSE AS-IS | Supporting state persistence, contention, and uncertainty boundary |
| BriefWise fresh local replay | REPACKAGE / INDEX | Supporting legal workflow replay |
| FastPath canonical replay certificate | REPACKAGE / INDEX | Supporting compact canonical-record replay |
| StormWise | REPACKAGE / INDEX | Optional exact-arithmetic weather instance |
| CleanWaterWise | REPACKAGE / INDEX | Optional environmental state-routing instance |
| VerdictBridge Demo 1 | REPACKAGE / INDEX | Historical legal replay instance |
| Replayable Damages Mini Demo | REPACKAGE / INDEX | Fixed arithmetic and archive identity |
| JoyWise Afterglow | REPACKAGE / INDEX | Text encoding and serialization identity |
| Erdős 124 | REPACKAGE / INDEX | Fixed-scope mathematical replay |
| Erdős 390 | REPACKAGE / INDEX | Exact rational certificate replay |
| Root README | NEEDS SMALL UPDATE | Link to this index and keep structure/count language current |
| New demonstration gap | NEW DEMO REQUIRED | No new demonstration is required for the initial curated track; existing evidence covers the five reviewer questions |

## Current evidence boundary

The primary set demonstrates system-level controlled/replayable execution under declared conditions. It does not require a single universal evaluator or serializer. A future version/runtime comparison could strengthen question 05, but it is not required for this initial curated track.
