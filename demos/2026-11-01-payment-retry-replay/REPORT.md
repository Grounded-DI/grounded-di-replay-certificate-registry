# Payment retry: measured local demonstration

## Two populations

**Historical private test:** The retained private package recorded a DI² v0.3.1 memory-mode gate and a synthetic effect recorder. Its first attempt had one matching unprotected case and seven setup errors: the fixture registered a policy-disallowed operation name. A corrected registration produced eight of eight expected test-function outcomes, including the new-ID limitation. These are historical results, not rerun here. The original archive is retained privately; its SHA-256 is `f57994684ec25618be889db67d228b889e65fc8f5f93b4931888d5a09722144b`.

**Public test:** A separately authored Python illustration implements its own simple in-memory gate and file recorder. It was freshly executed twice, in separate directories, with nine matching expected outcomes per run. Each of its three declared canonical JSON artifacts matched byte for byte. It does not import or execute the private gate, and its behavior does not prove behavioral equivalence with that implementation.

## Public observations

| Synthetic case | Observed statuses | Local effects |
|---|---|---:|
| Unprotected repeated call after lost responses | UNKNOWN, UNKNOWN | 2 |
| Approved unchanged action | RELEASED | 1 |
| Effect, lost response, same-ID retry | UNKNOWN, HELD | 1 |
| Changed recipient or changed amount | DENIED, separately | 0 each |
| Missing approval or at expiry | DENIED, separately | 0 each |
| Two individually approved distinct actions | RELEASED, RELEASED | 2 |
| Same business payload with a separately approved new ID | UNKNOWN, RELEASED | 2 |

For the same-ID case the script separately read the local effect file and found one matching row. That file is written and read by one trusted test environment; it is not an external attestation. The unprotected baseline is an intentionally unguarded function, not a model of a vendor's defaults. The new-ID test is an expected demonstration of a limitation and is not a pass for business-level deduplication.

## Boundary

The illustrative gate binds the supplied request object and synthetic approval before invocation, records consumption in memory, and leaves a lost-response result unresolved. It does not authenticate an approver, persist across restarts, handle concurrent requests, verify a real external effect, or prevent direct access to the provider function. It does not deduplicate logically identical actions that have different IDs. No provider, real payment, live account, hosted model, or network call is part of this demonstration.

The canonical boundary covers only the three JSON artifacts identified in the verification record. Two fresh executions generated them; they were not obtained by copying prior results. Python version and platform are recorded separately and are outside canonical bytes. A matching hash establishes equality of the selected bytes, not correctness of a real financial transaction or independent certification. The checksums are unsigned and self-issued.
