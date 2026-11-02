# ReleaseGate V3 — lost confirmation and local recovery

In the frozen baseline, a local process fsynced the pre-write record, logged one write attempt, wrote and fsynced the fictional candidate, then exited before recording or returning success. A fresh retry found the matching record and destination bytes and returned ALREADY_PRESENT without another write attempt. Two fresh baseline executions matched all seven canonical artifacts directly and by SHA-256 against prewritten expectations.

[Verification](verification.json) · [Runnable reproducibility package](ReleaseGate_V3_Reproducibility.zip) · [Clean extraction recheck evidence](ReleaseGate_V3_Extraction_Recheck.zip)

All 12 scenarios passed with zero failures, errors or skips. Tests cover normal writing, interruption before write, lost confirmation, same-request retry, mismatched or partial destination bytes, missing or inconsistent pre-write record, changed candidate under the same request, a new request ID, and coherently rehashed tampering. A different request ID with the same bytes is held because the retained record does not bind it to that request.

The separately implemented project checker recalculates baseline boundaries 1–6 from the request, policy and observed local files, and verifies their commitment. It shares the project, specification, inputs, host, Python and JSON/SHA-256 primitives. Matching unsigned local records and bytes support a limited recovery decision; they do not authenticate the actor or establish the historical cause of the file.

The test uses trusted local processes and an uncontended directory. It fsyncs file contents, not parent directories; injected process exits do not establish power-loss durability or arbitrary filesystem crash safety. No distributed exactly-once delivery, production deployment, external certification or universal model determinism is claimed. The clean extraction recheck is retained separately to avoid archive self-reference.
