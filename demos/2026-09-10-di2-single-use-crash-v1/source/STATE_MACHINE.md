# State machine and transaction boundary — defined before implementation

An explicitly enrolled authorization starts UNUSED. Request handling takes a bounded advisory process lock shared by this installation and validates the durable store, enrollment, request tuple, policy, report and clock.

1. UNUSED -> RESERVED is committed durably before any export-open attempt. This consumes the authorization even if no file is eventually created.
2. RESERVED -> COMPLETED is committed only after exclusive file creation, write, file fsync and directory fsync succeed. Success acknowledgment occurs after this commit.
3. On a subsequent request, RESERVED -> UNCERTAIN is committed. No export is attempted. Absence of a file does not restore UNUSED; presence of a matching file does not become an unrecorded success.
4. COMPLETED remains COMPLETED. Retry returns ALREADY_COMPLETED only after matching the existing report bytes; it never writes another file.
5. UNCERTAIN remains UNCERTAIN. Retry returns UNCERTAIN and never writes.
6. Invalid bindings, expiry, changed policy, or malformed/missing storage produce a refusal without export. No automatic enrollment or state reset occurs in request handling.

A process lock covers the sequence; SQLite commits with synchronous=FULL establish reservation and completion checkpoints. The filesystem export is not atomic with the SQLite commit. The deliberate conservative response to that gap is retained uncertainty, not exactly-once completion.

Crash points tested: committed reservation before export; flushed file before completion commit; completed commit before acknowledgment. Actual worker processes are stopped at these points and killed by the test runner. A fresh process retries the request.

Guarantee under the stated cooperative local-process boundary: at most one export creation attempt per authorization after a durable reservation, with possible noncompletion or uncertainty. This is not exactly-once delivery, system-wide enforcement, power-loss certification, or resistance to malicious same-account/root replacement of state and evidence. Database/enrollment rollback together is outside the protection boundary. Physical roots are fresh instances of the logical demo scope, not globally authenticated resource identities.

Replay validates the recorded order and its file bindings. A new concurrency run can have a different winner/order and hash; the verifier does not equate deterministic replay of a history with deterministic scheduling.
