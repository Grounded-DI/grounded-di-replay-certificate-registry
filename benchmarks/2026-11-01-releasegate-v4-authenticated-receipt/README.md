# ReleaseGate V4 — authenticated receipt and planted-file control

Two fresh local baselines matched all seven frozen artifacts byte for byte and by SHA-256. Fifteen registered scenarios passed with zero failures, errors or skips. In the lost-confirmation baseline, the receipt and candidate file existed without an acknowledgement; a fresh retry recognized the authenticated receipt and matching bytes without another gate write.

[Verification](verification.json) · [Runnable reproducibility package](ReleaseGate_V4_Reproducibility.zip) · [Clean extraction recheck](ReleaseGate_V4_Extraction_Recheck.zip)

Missing or unsigned receipts, untrusted-key tags, altered fields, receipts bound to another request, changed candidates, changed request identity, and different or partial destination bytes led to HOLD. The separate checker rejected rehashed changes to receipt and decision artifacts. The checker recalculates six baseline artifacts and validates their commitment; it shares the project, keys, inputs, host, Python and HMAC/JSON/SHA-256 primitives.

## Planted-file result

The fixture first generated a valid pre-write receipt and stopped before the gate wrote. The fixture then independently planted matching candidate bytes. Recovery returned ALREADY_PRESENT with zero gate write attempts, despite one fixture write. All seven canonical outputs matched the lost-confirmation baseline byte for byte. Thus the local check could not distinguish those two histories.

Both HMAC keys are deliberately PUBLIC TEST FIXTURES, not real secrets. Under a hypothetical trusted-key assumption, the tag supports integrity and possession of that key; it does not identify a person, authenticate when a receipt was created, prove who wrote a file, or prove an effect occurred. Because the fixture key is published, it gives no real-world authentication. Same-request retries remain allowed; no general anti-replay service is demonstrated.

The process and uncontended local directory are trusted. File contents are fsynced but parent directories are not. Injected process exits are not power-loss tests. No production readiness, secure key custody, trusted timestamps, external certification, arbitrary crash safety, distributed exactly-once delivery, or universal model determinism is claimed. The clean-extraction recheck is retained separately to avoid archive self-reference.
