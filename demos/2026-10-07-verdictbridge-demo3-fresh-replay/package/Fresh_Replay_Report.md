# Fresh_Replay_Report

- Source PDF: [Fresh_Replay_Report.pdf](https://github.com/Grounded-DI/grounded-di-replay-certificate-registry/blob/main/demos/2026-10-07-verdictbridge-demo3-fresh-replay/package/Fresh_Replay_Report.pdf)
- Source Git blob SHA: `92e53ff18b7d99b29b76c78b07baced3afe6fe69`
- Source SHA-256: `8454e9a250ade997a3a2a76aa63416cb6f34833cb9502544580eadc3017bf329`
- Page count: 2
- Byte size: 6518
- Extraction method: `pdftotext -layout` (Poppler)
- Classification: `TEXT-EXTRACTABLE` in the Phase 1 inventory

Provenance: This is a derived machine-readable companion. The original PDF is unchanged. The text below is the direct `pdftotext -layout` output; no OCR, summarization, rewriting, or silent correction was applied. Literal form-feed page separators from the extractor output are retained.

## Raw extracted text

~~~text
 VerdictBridge Demo 3
 Fresh local replay
 PASS | October 7, 2026 | Local review copy

 Exactly the same declared output under the same frozen execution conditions, with receipts showing what
 actually ran, SHA-256 hashes, and direct byte comparisons. Material changes produce a specified changed
 result or refusal.

 Measured outcome
 Three fresh evaluator processes (64149, 64150, 64151) produced all five canonical artifacts with matching
 SHA-256 hashes and direct byte equality. All fifteen artifacts also match their pinned historical counterparts
 directly. Zero byte differences were observed. This is a replay of the existing closed-world benchmark, not a
 new benchmark.

 Strict liability, negligence and compensatory damages: DENY_SUMMARY_JUDGMENT. Punitive damages:
 GRANT_SUMMARY_JUDGMENT. Overall motion: GRANTED_IN_PART_DENIED_IN_PART. Sam Reed:
 EXCLUDED_AND_NOT_USED. Jury instruction coverage: PASS. VerdictReady: YES. Export authorization:
 true.

 Fresh refusal evidence
 The candidate relying on Sam Reed to preserve punitive damages was rejected by the separate verifier with
 expected exit code 2. Failed rule: L015 / F051-F054 / L020. Failed verifier gates: VB-D-EAUR,
 VERDICTREADY-GATE and EXPORT-GATE. The export boundary also recorded a legal-disposition mismatch
 at VB-B-MOCC.

 VerdictReady NO; export_authorized false; export files opened 0; bytes written 0; final output inventory
 []. This was a recorded substantive refusal, not an unexplained crash or missing result.

 Controls and execution discipline
 All seven prescribed altered-copy controls were rejected: reference law, restored cost fact, wrong disposition,
 Reed in trace, missing export, forged receipt and changed ZIP bytes. The intentionally missing artifact tests
 completeness only. Oracle independence, baseline recalculation by the new evaluator and forged-disposition
 export refusal also passed.

 The pinned ZIP, its manifest and the evaluator/verifier hashes passed preflight integrity checks. Benchmark
 steps ran sequentially with a lock and 120-second process-group timeouts; all completed with their expected
 exits. Commands, stdout/stderr, fresh receipts and environment records are included. Existing evidence stayed
 unchanged and replay automation stayed paused.

 Source and interpretation
 Pin: ac3a8cd522718235d2a7154c728566614086a809. The original reference evidence remains reference only. The evaluator was newly
 implemented for the earlier Demo 3; this activation executed that unchanged implementation. Its verifier is separate internal code. This is
 not original-engine execution, universal model determinism, unaffiliated validation, external certification or legal compliance.




Fresh replay | Internal verification | No external certification                                                                               1
 Byte receipts and scope
 Each digest below was measured independently for fresh Runs A, B and C; all three match the pinned
 expected value and historical bytes. HASHES.md lists all fifteen observations explicitly.

 01_canonical_input.json | A = B = C = pinned | 14996 bytes
 c53a77a0df2032fc2931bfb1793991d274c98ce1a6d2f7aef5534bc3ae0df561

 02_normalized_record.csv | A = B = C = pinned | 14563 bytes
 99aa74d84fe9e33cedaf9a4820eb846ce5618f0aa74e8951241ba1347ada93cc

 03_gate_matrix.json | A = B = C = pinned | 4181 bytes
 242401fedf2c6a01b0cc376e8734cfeafff180f5d669ae9775e43a95c2014775

 04_verdictbridge_assessment.txt | A = B = C = pinned | 2348 bytes
 90faa90efa8f79aab956427479788e616f87b0178606d4f2563535cccd5a0378

 canonical_run.zip | A = B = C = pinned | 36608 bytes
 947314014bd8251f8cfb67d080bd7244d648752e9532aee109b85cf5f836324c


 What was frozen; what changed
 Inputs, controlling rules, expected outcomes, evaluator/verifier source and canonical serialization were
 unchanged. Each of the three fresh runs used CPython 3.9.6, Darwin 25.6.0, arm64, with the same recorded
 configuration. Runtime receipts differ from the pinned receipts only in process ID and start/finish timestamps.
 Those fields are outside the five-artifact identical-byte boundary.

 The historical receipt lacks an OS/interpreter inventory, so identical historical execution conditions cannot be
 established. Artifact equality to that historical release was measured directly. The new complete package
 necessarily differs because it includes fresh receipts, verification records and this report. No complete-package
 identity claim is made.

 Limits of the result
 Three successful executions establish the observed finite replay, not an always-identical guarantee. No
 generative model was called. The tested changes cover specified fact and integrity controls; they do not cover
 every possible material change. Cooperative export refusal is not system-wide enforcement or human
 shutdown of an AI model.

 Review and bindings
 Start with verification/measured-results.json, execution/commands.json, environment.json and the fresh replay/
 directory. Inspect the verifier and invalid-control evidence. The unsigned replay certificate binds the delivered
 evidence; SHA256SUMS.txt binds the certificate. The complete ZIP hash is provided separately to avoid
 self-reference.

 Next step: an unaffiliated reviewer authenticates the pinned source/package and reviews or independently
 reproduces the bounded result in a newly recorded environment. Keep that review distinct from this internal
 verification. Nothing has been published or sent.




Fresh replay | Internal verification | No external certification                                                     2

~~~
