# DI² Replayable Authorization Demo

**An authorized export succeeds. A changed destination is rejected before writing. The decision can be reproduced locally.**

This record contains a small synthetic cybersecurity demonstration combining an action proposal generated through Grounded DI OS with a separate, runnable Python authorization harness.

## Downloads

- [Demo ZIP](DI2_Replayable_Authorization_Demo_20260910_1110.zip)
- [ZIP SHA-256](DI2_Replayable_Authorization_Demo_20260910_1110.zip.sha256.txt)
- [Local replay certificate](replay-certificate.json)

Public packaging revision: the certificate classification is `LOCAL_TESTS_PASSED`. Only certificate wording and package checksums changed; evaluator, inputs, results, and replay identity are unchanged. The detailed serialization specification and runnable source are inside the ZIP.

## What this demonstrates

An operator authorizes exporting a synthetic report to `approved/report.txt`. The authorization binds:

- The report’s SHA-256.
- The permitted action.
- The destination.
- The policy version.
- The declared scope and synthetic state.

The harness checks those bindings before opening an output file. Changing the destination to `changed/report.txt` while retaining the original authorization causes rejection.

## Executed results

| Test | Observed result |
|---|---|
| Original authorized action | **PASS** — report exported with matching bytes |
| Changed destination, original authorization | **PASS** — rejected with `DESTINATION_MISMATCH`; zero write-open attempts |
| Original action evaluated again | **PASS** — report exported in a fresh isolated case directory |
| Fresh-process replay | **PASS** — regenerated canonical bytes and SHA-256 matched |
| Altered report in a separate copy | **PASS** — verification rejected the altered content |
| Altered action in a separate copy | **PASS** — replay identity diverged |
| Missing saved export in a separate copy | **PASS** — verification rejected missing evidence |
| Untouched original after negative controls | **PASS** — unchanged and successfully reverified |
| Extracted ZIP acceptance and checksums | **PASS** |

Each execution case uses a separate instance of the logical `demo_directory` scope.

## Application and execution boundaries

**Grounded DI OS** created the persistent project, generated the action proposal through its assistant, and saved the response. Reloading the saved conversation restored that response.

**The bundled Python harness** performed authorization checks, actual file exports, rejection, and deterministic replay.

The assistant’s response explicitly labels its cases as expected outcomes and says `not_executed`. Those predictions are not execution evidence. Execution evidence comes from the separately executed harness and its saved outputs.

This demonstration does not establish that the installed Grounded DI OS application or ShieldBot implements this export gate.

## Reproduce locally

Download and extract `DI2_Replayable_Authorization_Demo_20260910_1110.zip`.

Requirements: Python 3.9+ on macOS or a POSIX platform supporting directory descriptors and `O_NOFOLLOW`. No third-party Python packages or model calls are required for replay.

From the extracted demo directory:

```sh
python3 -B verify.py
python3 -B acceptance.py
shasum -a 256 -c SHA256SUMS.txt
```

- `verify.py` starts a fresh process, reruns the included evaluator, performs fresh exports in temporary directories, and checks the regenerated identity and saved evidence.
- `acceptance.py` runs negative controls against separate copies and reverifies the untouched original.
- `SHA256SUMS.txt` covers the other files in the bundle.

A nonzero verifier or acceptance exit code indicates failure. Replay creates temporary synthetic files and removes its temporary directories afterward.

## Replay identity

**SHA-256 of the canonical replay-identity bytes:**

```text
9192da71d870ddcdcb9dfddfc2b695a00365acf87910cee9b4047590d5ac4632
```

The identity binds the kernel source hash, exact input-file hashes, regenerated decisions, and exported-file hashes.

Serialization uses the documented custom format `DI2-ASCII-JSON-LF-1`: restricted ASCII JSON values, sorted object keys, compact separators, and one terminating LF. It is not presented as full JCS compliance.

Timestamps, physical output directories, assistant wording, and model/run metadata are outside the deterministic replay identity. The package checksums cover the saved supporting files separately. Model and run identifiers unavailable in the observed application interface are recorded as unavailable.

## Included evidence

- Submitted prompt and captured assistant response.
- Synthetic report, policy, authorization, and action records.
- Runnable `demo.py`, `verify.py`, and `acceptance.py`.
- Execution results and exported reports.
- Canonical replay identity and SHA-256.
- Verification and negative-control results.
- Application provenance and local replay certificate.
- Detailed README and file checksums.

The assistant response was captured from rendered accessibility text; original provider formatting is not attested.

## What the result establishes—and its limits

The changed destination was rejected before this harness opened an export file. Fresh replay recomputed the decisions rather than accepting stored `PASS` values or merely comparing previously saved hashes.

Replay uses the **same versioned evaluator implementation**, not an independently implemented second evaluator.

The authorization is a synthetic operator record created for this demonstration. It is not an authenticated organizational approval. The supplied state is synthetic data, not independently measured operating-system permissions.

The local replay certificate is unsigned and self-issued. It records local test results; it is not third-party certification. Package hashes do not prevent an attacker from replacing the entire package and its checksums together.

This demonstration does not establish:

- System-wide enforcement or enterprise readiness.
- Resistance to a hostile user account, administrator, or compromised filesystem.
- Revocation, expiry, one-time authorization, or comprehensive race protection.
- Identical model generation, correct threat detection, or superiority over other security products.

Only synthetic data was used. No live containment actions or changes to system security settings were performed.

## Project context

This is a Grounded DI / DI² demonstration of explicit authorization boundaries and reproducible execution decisions.

The practical question it tests is:

**When a proposed action changes after authorization, does the execution gate refuse it—and can the resulting decision be reproduced from the saved evidence?**
