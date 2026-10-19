# Published_Replay_Report

- Source PDF: [Published_Replay_Report.pdf](https://github.com/Grounded-DI/grounded-di-replay-certificate-registry/blob/main/demos/2026-10-08-verdictbridge-demo3-published-replay/package/Published_Replay_Report.pdf)
- Source Git blob SHA: `c6e2e5a17aaa23ea60e6e3942792847b8708e36e`
- Source SHA-256: `9a9813d6e6cd1cc9e3631d82609f4a3d442391eaa2aed77943e589ea2f88393f`
- Page count: 2
- Byte size: 6395
- Extraction method: `pdftotext -layout` (Poppler)
- Classification: `TEXT-EXTRACTABLE` in the Phase 1 inventory

Provenance: This is a derived machine-readable companion. The original PDF is unchanged. The text below is the direct `pdftotext -layout` output; no OCR, summarization, rewriting, or silent correction was applied. Literal form-feed page separators from the extractor output are retained.

## Raw extracted text

~~~text
 Demo 3 | Published-release replay
 PASS within stated scope | October 8, 2026 | Local and unpublished

 A fresh local replay of the existing closed-world Demo 3 benchmark, using the unchanged published evaluator,
 separate internal verifier and frozen case. This is not a new benchmark or unaffiliated validation.

 Download verified before execution
 Source commit: 46903262313a164642aea4f6a496b398c2d120b6. The public ZIP was downloaded from that
 exact commit. Its expected SHA-256 matched; all 127 manifest entries and 126 certificate bindings passed
 before evaluator execution. The received ZIP and extracted evidence remain unchanged.

 Public ZIP SHA-256:

 8f401a26711b423055079423e766558e1b2ec82309bbc470d469969d5bd448cc


 Three fresh processes; declared result verified
 New evaluator process IDs: 74180, 74181, 74182. Execution was sequential and nonoverlapping with finite
 timeouts. Five canonical artifact types match across the new runs and against both the published replay and
 older pinned artifacts, using SHA-256 and direct byte comparisons. Zero byte mismatches were observed.

 Strict liability, negligence and compensatory damages: DENY_SUMMARY_JUDGMENT. Punitive damages:
 GRANT_SUMMARY_JUDGMENT. Overall motion: GRANTED_IN_PART_DENIED_IN_PART. Sam Reed:
 EXCLUDED_AND_NOT_USED. Jury instruction coverage: PASS. VerdictReady: YES. Export authorization:
 true.

 Actual hearsay refusal; prescribed controls
 The separate verifier rejected the hearsay candidate with expected exit 2:
 INADMISSIBLE_EVIDENCE_RELIANCE, rule L015 / F051-F054 / L020; gates VB-D-EAUR,
 VERDICTREADY-GATE, EXPORT-GATE. The export boundary also recorded
 LEGAL_DISPOSITION_MISMATCH / VB-B-MOCC.

 VerdictReady NO; export_authorized false; export files opened 0; bytes written 0; final output inventory
 []. The verifier checked the empty open audit and actual export directory. This was a substantive refusal, not an
 unexplained crash.

 Seven tamper controls were rejected for the expected reasons: reference law, restored cost fact, wrong
 disposition, Reed in trace, missing export, forged receipt and changed ZIP bytes. The deliberate missing-file
 test checks completeness only. Oracle independence, baseline recalculation and forged-disposition export
 refusal passed.

 Provenance and limits
 Preserved reference evidence, the previously implemented local evaluator, its separate internal verifier and fresh measured executions are
 distinct layers. No original-engine execution, universal model determinism, external certification or legal compliance is claimed. Automation
 stayed paused; no publication or outreach occurred.




Published-source replay | Internal verification | No external certification                                                                      1
 Canonical bytes and environment
 Each hash below is identical for fresh Runs A/B/C and the published artifacts. HASHES.md contains all fifteen
 fresh measurements. Canonical ZIP entries retain January 1, 1980 metadata. Real execution times and
 process IDs remain in separate receipts.

 01_canonical_input.json | 14996 bytes | all comparisons PASS

 c53a77a0df2032fc2931bfb1793991d274c98ce1a6d2f7aef5534bc3ae0df561

 02_normalized_record.csv | 14563 bytes | all comparisons PASS

 99aa74d84fe9e33cedaf9a4820eb846ce5618f0aa74e8951241ba1347ada93cc

 03_gate_matrix.json | 4181 bytes | all comparisons PASS

 242401fedf2c6a01b0cc376e8734cfeafff180f5d669ae9775e43a95c2014775

 04_verdictbridge_assessment.txt | 2348 bytes | all comparisons PASS

 90faa90efa8f79aab956427479788e616f87b0178606d4f2563535cccd5a0378

 canonical_run.zip | 36608 bytes | all comparisons PASS

 947314014bd8251f8cfb67d080bd7244d648752e9532aee109b85cf5f836324c


 Environment comparison: recorded fields match
 CPython 3.9.6, Darwin 25.6.0 and arm64 match the published replay. The Python executable binary SHA-256,
 implementation, locale, timezone names and selected environment variables also match. All nine recorded
 comparison fields agree. See environment-comparison.json for the actual values.

 The published executable path was redacted, so path identity is UNKNOWN; binary hashes were compared
 instead. Unrecorded machine state is not assessed. The older historical receipts lack an OS/interpreter
 inventory. No claim of complete historical environment identity follows from the recorded-field matches.

 Expected differences; bounded conclusion
 Run receipts differ from the published replay only in process ID and start/finish timestamps. The new
 environment timestamp, logs, report and complete delivery ZIP also differ. Canonical artifact identity,
 substantive internal verification and environmental comparability are separate findings.

 Three successful executions establish this observed finite replay, not an always-identical guarantee. No
 generative model was called. Specified fact/integrity controls do not cover every possible change, and
 cooperative export refusal is not system-wide enforcement.

 Review-ready evidence
 Start with verification/measured-results.json, execution/commands.json, the fresh replay/ folders and
 environment-comparison.json. The local certificate binds delivered evidence; the manifest binds the certificate;
 the complete ZIP has an external checksum. The next concrete step is unaffiliated inspection of the source,
 receipts and refusal evidence, with the reviewer recording their own scope and observations.




Published-source replay | Internal verification | No external certification                                         2

~~~
