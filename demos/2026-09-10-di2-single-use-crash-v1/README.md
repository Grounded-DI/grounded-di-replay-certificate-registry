# DI² Single-Use Authorization and Crash Recovery — v1

**Can one authorization create a second export when requests compete, retry, or recover after a crash?**

In this bounded local demonstration, 20 separate processes competed for one authorization: **one completed export and 19 duplicate acknowledgments, with one export-open attempt in total.** All worker outcomes are preserved.

This extends the [expiry and policy-change demonstration](https://github.com/Grounded-DI/grounded-di-replay-certificate-registry/tree/main/demos/2026-09-10-di2-expiry-policy-v1). Earlier records remain unchanged.

## Downloads

- [Complete ZIP](DI2_Single_Use_Crash_Replay_v1_20260910.zip)
- [ZIP checksum](DI2_Single_Use_Crash_Replay_v1_20260910.zip.sha256.txt)
- [Local certificate](replay-certificate.json)
- [Browsable source and evidence](source/)

Certificate paths are relative to source/ or the extracted ZIP folder.

[ZIP and clean-checkout validation](publication-validation.json) passed.

## Actual results

| Scenario | Observed result |
|---|---|
| Valid request followed by duplicate | One completion; ALREADY_COMPLETED on retry; same file inode |
| 20 processes released from a readiness barrier | One completion, 19 ALREADY_COMPLETED results; 20 distinct process IDs |
| Two distinct authorizations and destinations | Two completed exports |
| Same authorization ID, altered report binding | REFUSED; no export |
| Same authorization ID, altered destination | REFUSED; no export |
| Expired authorization | REFUSED; no export |
| Changed full policy content | REFUSED; no export |
| Missing database, malformed schema, corrupted database, missing authorization row | REFUSED; no reset, no export |
| SIGKILL after reservation, before file creation | Recovery retains UNCERTAIN; no file, no new write |
| SIGKILL after file flush, before completion commit | Recovery retains UNCERTAIN; existing file preserved, no new write |
| SIGKILL after completion commit, before acknowledgment | Retry returns ALREADY_COMPLETED; existing file preserved |
| Untouched baseline | State/history and exports unchanged; replay passes |

**14 scenarios, three actual SIGKILL crash points, and six altered-copy controls passed.** UNCERTAIN is a deliberately retained incomplete outcome, not a successful export acknowledgment. Repeated requests in that state are refused with UNCERTAIN_NO_RETRY.

## What ran where

Grounded DI OS generated the saved synthetic proposal and acknowledged saving its response. Reload recovered it. The response explicitly says not_executed.

A separate Python harness implemented and tested the execution gate. This is not a demonstration that the installed Grounded DI OS or ShieldBot application enforces these actions. The operator authorization is a synthetic record created under the user's demo instruction, not an authenticated organizational approval.

Model and run identifiers unavailable in the observed UI are recorded as null. The captured response preserves rendered JSON text; original provider byte formatting is not attested. No private application runtime source is included.

## State machine and persistence

The design was recorded in STATE_MACHINE.md before implementation:

```text
UNUSED -> RESERVED -> COMPLETED
                    \-> UNCERTAIN (on recovery without a completion record)
```

Reservation consumes the authorization. There is no transition back to UNUSED.

The gate uses a bounded advisory process lock across reservation, export, and completion. SQLite records reservation and completion in separate transactions with synchronous=FULL. The writer uses exclusive file creation and fsync for file and directories. Request handling opens existing storage only; initialization is an explicit separate operation.

Enrollment binds the unique authorization identifier, report hash, destination, action, canonical full-policy hash, scope, and validity interval. Storage checks compare enrolled records, states, and the complete hash-linked transition history. Expiry uses an explicit injected Unix-millisecond time with issued_at <= time < expires_at. This record tests process persistence and races, not a trusted clock or live revocation service.

The SQLite transaction and filesystem export are not one atomic operation. A crash can leave a reservation without completion. Recovery refuses to guess: a missing file does not restore permission, and a present file does not manufacture a completion acknowledgment.

The claimed property is **at-most-one export creation attempt per authorization within this cooperative store**, with possible noncompletion or uncertainty. Exactly-once completion is not claimed. A new separate store is a new logical demo instance; this is not global deduplication across stores.

## Reproduce

Requires Python 3.9+ and macOS/POSIX facilities including flock, directory descriptors, O_NOFOLLOW, SIGSTOP and SIGKILL. SQLite is provided by Python. No model calls, network access, private configuration, or third-party packages are required.

From the source directory or extracted ZIP folder:

```sh
python3 -B verify.py
python3 -B acceptance.py
shasum -a 256 -c SHA256SUMS.txt
```

- **verify.py** replays the saved transition order using the separately implemented reference checker, recomputes bindings, and checks exported bytes. It does not execute the gate or consume stored PASS labels as proof.
- **acceptance.py** reverifies the saved history, tests six altered copies, and runs a new full experiment using new worker processes and three real SIGKILL crash tests. Only Popen child handles created by the test runner are killed. It checks the new run with the reference checker, then reverifies the untouched originals.
- **run_suite.py NEW_DIRECTORY** generates another full experiment into a nonexistent output directory. It never overwrites a prior record. New experiment histories are evidence, not automatically sealed certificates.

Temporary runtime stores are isolated and removed after the suite. Durable state persists between each worker process and recovery process during the experiment. Saved evidence includes consistent logical SQLite snapshots exported under the process lock, worker requests/results, actual checkpoint observations, and report files. Physical SQLite database pages are not included or replayed. Failed-store observations are checked against the recorded fault and reproduced by fresh acceptance tests; they are not an independent forensic database examination.

The package works without empty directories. A missing expected report or scenario fails verification. Nonzero exit means failure.

## Replay identity and concurrency

Replay SHA-256:

`c02ff6c5802c398b4a20a75c48a05ad11a32c766fd507bc2f16e16befb3351c8`

`replay-identity.json` is the exact canonical byte file. Identity binds the eight listed implementation/design files, report hash, all evidence-file bytes, and freshly derived history-check results. Worker process IDs and observed event order are retained in evidence and therefore bound. The standalone checker validates request bindings, chain sequence, allowed state transitions, reservation ownership, completion hashes, worker outcomes, and report inventories.

A new concurrency run may have a different winner, event order, process IDs, and identity. Acceptance checks its safety outcomes rather than demanding identical scheduling or concurrent-run bytes. Matching canonical bytes apply to replay of the **same recorded history**.

Serialization: DI2-ASCII-JSON-LF-1, a restricted custom format, not full JCS. Supported values are null, booleans, exact-range integers (+/-9007199254740991), lists, dictionaries with string keys, and printable ASCII strings plus LF. Keys sort lexicographically, array order is retained, JSON uses compact separators and ASCII escaping, and bytes end in one LF. Duplicate input keys and nonfinite numbers are rejected. Physical workspace paths and assistant wording are outside the replay identity; supporting deliverables are separately checksummed.

## Reference checking and negative controls

reference_check.py imports no gate, worker, or suite implementation. It shares codec.py serialization, hashing and JSON-reading primitives. Both implementations were authored in the same task against the same specification; this is not external independent verification.

Altered-copy tests rejected:

- changed report bytes: EXPORT_BYTES_MISMATCH;
- invented completion with rebuilt event hashes: INVALID_COMPLETION;
- duplicate reservation with rebuilt event hashes: INVALID_RESERVATION;
- missing worker: UNACCOUNTED_EVENT_WORKER;
- missing case: MISSING_SCENARIO;
- changed recorded clock: REQUEST_EVENT_BINDING.

## Limitations

The certificate is unsigned and self-issued, classification LOCAL_TESTS_PASSED. It reports local observations, including retained uncertainty; it is not third-party certification.

The gate protects its own cooperative processes. It does not intercept unrelated writers, authenticate an organization, stop a malicious same-account/root process, guarantee persistence through power loss or hardware failure, or detect an attacker replacing or rolling back database, enrollment, code, and evidence together. Path checks do not constitute comprehensive protection against a compromised parent filesystem. Advisory locks can be bypassed by other programs.

A crash during an untested partial-write window may leave partial bytes and a reservation; no automatic retry is authorized. Only the three specified post-checkpoint process-kill windows were tested. Broader I/O failure, power-cut, distributed-store, and hostile-clock validation remain unverified.

All actions and data are synthetic. No installed applications or system security settings were changed, and no live containment was performed. No enterprise readiness, system-wide enforcement, malware-detection accuracy, or identical model generation is claimed.
