# DI² Authorization Expiry and Policy Replay — v1

**Approval does not survive expiry or a change to the policy it authorized.**

This synthetic demonstration extends the [destination-change record](https://github.com/Grounded-DI/grounded-di-replay-certificate-registry/tree/main/demos/2026-09-10-di2-authorization). The previous demonstration is preserved.

Grounded DI OS generated the saved proposal. A **separate local Python harness** enforced its own file-export boundary. This record does not claim an installed application enforcement feature.

## Executed results

| Case | Observed result |
|---|---|
| Valid authorization, unchanged policy | ALLOW; actual synthetic report exported |
| Expired after approval | DENY / EXPIRED; no export opened |
| Exactly at expiry | DENY / EXPIRED; strict upper boundary |
| Policy version changed after approval | DENY / POLICY_HASH_MISMATCH |
| Policy content changed, version unchanged | DENY / POLICY_HASH_MISMATCH |
| Missing, null, malformed authorization/policy/time | DENY with explicit invalid-evidence reason |
| Boolean/fractional time and invalid validity interval | DENY |
| Before issuance; changed action destination | DENY |
| Untouched valid inputs evaluated again | ALLOW; actual export in a fresh isolated directory |
| Bounded real-clock expiry | Initially ALLOW, then DENY / EXPIRED with zero write-open attempts |

**25 recorded cases, 10 additional boundary checks, and six altered-copy controls passed.** All recorded decisions agreed with a separately implemented reference evaluator. Fresh processes reproduced canonical bytes and verified saved exports. Original files remained unchanged across acceptance testing.

The negative controls altered report bytes, expiry evidence, policy content without its version, a saved export, a saved decision, and evaluator source. All were rejected. Exact rejection reasons are in negative-controls.json.

## Reproduce

Python 3.9+ on macOS or POSIX with directory-descriptor operations and O_NOFOLLOW. No third-party packages or network/model calls are needed.

Run from this source directory (the extracted ZIP folder, or the repository's `source` directory):

```sh
python3 -B verify.py
python3 -B acceptance.py
shasum -a 256 -c SHA256SUMS.txt
```

`verify.py` starts a fresh evaluator process, reruns the recorded input snapshots, compares the kernel with the reference evaluator, performs fresh synthetic exports in temporary directories, and checks recorded results and exported bytes. It does not accept stored PASS values as verification.

`acceptance.py` additionally checks expected outcomes, probes both time boundaries, alters separate copies, performs a new bounded real-clock expiry test, and verifies the untouched original. Temporary files are confined to test directories and cleaned up. Any nonzero exit is failure. Empty directories are not evidence and need not survive Git checkout; actual file inventories are checked.

To create a new record with new real-clock timestamps, use a nonexistent destination:

```sh
python3 -B record.py /path/to/new-demo-record
```

This intentionally produces a new replay identity. It never overwrites a release. It copies the runnable implementation and creates new test evidence; it does not generate another assistant response or certificate.

## Time and policy semantics

Time values are nonnegative integer Unix milliseconds within the exact JSON integer range. Booleans, strings, fractional values, and missing times are invalid. Authorization requires:

```text
issued_at <= execution_time < expires_at
```

The gate samples its supplied clock after preparing/pinning the isolated output directory and immediately before validation and its write branch. A scheduler delay can occur between validation and the OS write; this is a check-time guarantee, not an atomic OS deadline guarantee.

The full canonical policy object is SHA-256 bound. The supported policy schema includes version, export_enabled, max_bytes, action, destination, scope, and state. Unknown or missing fields are rejected. A same-version change from max_bytes 4096 to 2048 invalidates the original authorization even though the report remains under both limits.

Every case stores separate approval and execution snapshots. All approval snapshots are actually evaluated as ALLOW before their execution snapshots are tested. These are supplied synthetic snapshots, not a live organizational policy service.

The initial real-clock test used a 250 ms authorization lifetime and a wait bounded by a monotonic timeout. Its wall-clock sample and observed result are saved. Replay injects that recorded historical time and reproduces that historical rejection; it does not claim the authorization is valid now. Each acceptance run separately tests new real-clock expiry. The local wall clock may be adjusted or controlled by a privileged attacker. No trusted time server, clock attestation, or anti-rollback clock is provided.

## Replay identity

SHA-256:

`08f6750447a0f923d1b175a436f9ef03f98d0b50b755b52e276aed05bb410fe8`

`evidence/replay-identity.json` contains the exact canonical bytes. Identity binds all seven runnable source files, exact bytes of the report, cases, recorded real-clock case/observation, and regenerated results. Real timestamps are explicit frozen inputs; changing them changes identity. Physical execution directory paths and assistant wording are outside this identity. Supporting files are separately bound by the certificate and SHA256SUMS.txt.

Serialization is **DI2-ASCII-JSON-LF-1**, a restricted custom format, not full JCS. Supported values are null, booleans, integers in +/-9007199254740991, lists, dictionaries with string keys, and printable ASCII strings plus LF. Keys sort lexicographically; arrays retain order; JSON is compact with ASCII escapes and exactly one final LF. Input JSON duplicate keys and nonfinite numbers are rejected. Deliberately invalid fractional clock inputs are preserved in raw cases.json, whose exact bytes are hashed; their result records use a string representation under invalid_number. Inputs are not silently rewritten to make hashes agree.

## Reference evaluator

`reference.py` implements its own validation and decision logic and imports no kernel functions. It shares only canonical serialization, JSON loading utilities where used by the runner, and SHA-256 primitives in `codec.py`. Both implementations were authored in the same Codex task against the same specification. Agreement is useful cross-checking; it is **not external independent verification**, and shared specification or serialization mistakes remain possible.

## Application provenance

The first Grounded DI OS request failed with “The matter request is invalid.” A shorter proposal-only retry succeeded. The successful response explicitly says not_executed. The application acknowledged saving it; reload recovered it and retained the earlier failure. Both prompts and the failure are preserved.

The response was captured from rendered accessibility text and screenshots; original provider formatting is not attested. Model/run identifiers unavailable in the observed UI are recorded as null rather than fabricated. No private runtime source is included.

## Execution boundary and limits

The authorization is a synthetic operator record, not a signed organizational approval. Report bytes and records are held as local snapshots. The writer uses a pinned isolated directory, no-follow opens, exclusive creation, and a literal allow-listed filename. Rejected actions do not reach its export-open branch; filesystem inventories independently check exported files. Directory creation during preparation is not report export.

No system-wide interception, external writer blocking, policy-revocation service, anti-replay nonce, organizational identity, hostile same-account/root resistance, or comprehensive concurrency protection is established. Another process can bypass this harness. Supplied scope/state is not independent OS permission evidence. Cases use separate instances of the logical demo_directory scope; physical roots are not authorization identities. A compromised parent filesystem or process is outside this demonstration's boundary.

The certificate is **unsigned and self-issued**, classification LOCAL_TESTS_PASSED. Hashes detect divergence against retained references; an attacker replacing all code, inputs, evidence, and checksums can replace the entire story. No enterprise readiness, threat-detection accuracy, identical model generation, or independent external certification is claimed.

Only synthetic data was used. No containment or system-security changes were performed.
