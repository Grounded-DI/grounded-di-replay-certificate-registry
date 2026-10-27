# Release record

Reference benchmark archive verified locally against its unsigned detached receipt; the verifier reported 116 members and SHA-256 497614c00216d7fe86886afdfd93aa7c08a5d65a590c38dd8a78e5380d80fa98. Starting repository head: 45967f8569ad3e56c47bcdb7b2a018ceac6401cd.

Before either computation the contract, inputs, stage methods, expectations, tests and release conditions were fixed. The coherent-wrong-result test implementation was refined before the first run to mutate the ledger and reissue its commitment while retaining the same input. No expected result was changed.

Both original processes and fresh reproductions used Python 3.12.14. Seven stage pairs matched by bytes and SHA-256. The five named tests in test.log passed with no failures, errors or skips. The input control changes a unit price; the output control adds a byte; the limit test exercises equality; the wrong-result control reissues a commitment over an altered ledger. The latter passes integrity and fails the fixed expected-value check. This is one local project-internal check; it is not external verification.

The standalone checksum list excludes itself. Verify checksums in this directory and reconcile the entire file list. The final verification command's contemporaneous output is a separate local release record, not part of the frozen manifest.
