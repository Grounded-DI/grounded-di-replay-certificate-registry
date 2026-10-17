# Registry inventory and fourth-lane shortfall

The registry was cloned read-only from `https://github.com/Grounded-DI/grounded-di-replay-certificate-registry` at retrieval time. Snapshot commit: `a7c5e0ffce8a7046f20d28286be1d414f3bb65a4`.

## Current demo directories

| Directory | Status for this request |
|---|---|
| `2026-09-10-di2-authorization` | Previously completed; excluded by command |
| `2026-09-10-di2-expiry-policy-v1` | Previously completed; excluded by command |
| `2026-09-10-di2-single-use-crash-v1` | Previously completed; excluded by command |
| `2026-10-05-verdictbridge-punitive-control-v1` | Previously completed; excluded by command |
| `2026-10-07-verdictbridge-demo3-fresh-replay` | Remaining complete executable replay candidate; ZIP SHA-256 `8f401a26711b423055079423e766558e1b2ec82309bbc470d469969d5bd448cc` |
| `2026-10-08-verdictbridge-demo3-published-replay` | Remaining complete executable replay candidate; ZIP SHA-256 `6e5399378479d8e7dc030f6c9139b93449978fd5cf57b39c5055e8eb4f05c5a6` |
| `nyc-exact-output-determinism` | Curated evidence index only; no executable package, archive, verifier, or canonical record of its own |

The two remaining candidates are two dated replays/public derivatives of the same VerdictBridge Demo 3 benchmark, not two distinct domain demos. No third or fourth complete executable demo is present in the current registry tree after applying the exclusion list.

## Exact reason for shortfall

The command requires four lanes but the registry contains only two non-excluded complete runnable replay packages. The NYC directory explicitly describes itself as a curated evidence index; its README links to already-listed evidence and supplies no runnable package or verifier of its own. Inventing a fourth lane or treating the index as an executable replay would violate the command.

No additional demo directory exists in the snapshot. The executor therefore must preserve this inventory and report the fourth-lane shortfall as `UNRESOLVED` rather than fabricate files or rerun an excluded replay.

