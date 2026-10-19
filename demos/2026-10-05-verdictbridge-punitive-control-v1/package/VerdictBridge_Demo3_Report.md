# VerdictBridge_Demo3_Report

- Source PDF: [VerdictBridge_Demo3_Report.pdf](https://github.com/Grounded-DI/grounded-di-replay-certificate-registry/blob/main/demos/2026-10-05-verdictbridge-punitive-control-v1/package/VerdictBridge_Demo3_Report.pdf)
- Source Git blob SHA: `8b47c5c46b3e746d74ae01f2f39eb3598c2197f1`
- Source SHA-256: `958564eca7f61913b820e0ed1e1b1a6979a41596a16abe0dfefe08b170e35bf4`
- Page count: 8
- Byte size: 17507
- Extraction method: `pdftotext -layout` (Poppler)
- Classification: `TEXT-EXTRACTABLE` in the Phase 1 inventory

Provenance: This is a derived machine-readable companion. The original PDF is unchanged. The text below is the direct `pdftotext -layout` output; no OCR, summarization, rewriting, or silent correction was applied. Literal form-feed page separators from the extractor output are retained.

## Raw extracted text

~~~text
 VERDICTBRIDGE / DEMO 3


 Selective legal outcome replay
 Five-hash byte reproducibility | Operator review | October 5, 2026


 DISPOSITION: PASS
 Case: Lane v. Apex Industrial Tools, Inc. VB-DEMO-0001-PUNITIVE-CONTROL

 Mission
 Remove the documented punitive-damages motive while preserving liability and compensatory evidence. Test
 the declared selective result in three fresh executions, compare all five canonical artifacts, and refuse an
 inadmissible-hearsay rescue attempt.

   Measured property                                      Result

   Selective legal result                                 Granted in part and denied in part; punitive damages dismissed at
                                                          summary judgment.

   Three-run five-hash / direct-byte match                PASS - all five layers, all three runs.

   Invalid hearsay control                                REFUSED - VerdictReady NO; export false; zero opens and zero bytes.

   Preserved original reference files                     PASS - all five hashes independently checked.


 Production context: Grounded DI OS via FastPath 6.1 Sol - Medium (operator-provided). Computation uses the included local
 Python evaluator; provider metadata is not attested.

 Implementation scope
 A newly implemented evaluator, operating on the same closed-world benchmark structure, produced the
 declared selective legal result reproducibly across three executions and correctly refused the
 inadmissible-hearsay control.

 Original Verdictbridge_demo-2 is reference evidence only. No original engine or native VerdictBridge implementation was
 executed. Public evidence release of local executions.




Grounded DI LLC | New local evaluator | Closed-world evidence                                                                 Page 1
 1 / Exact factual change
 All 20 stipulated authorities, questions, procedural posture, and other facts remain unchanged. The new case
 ID and declared expected outcomes are encoded before execution. F038 and F039 are exact restatements;
 only F037 and F040 have changed fact text.

 F037
 Apex marketing director Victor Hale rejected the proposed Zeta-9-specific warning recommended by Elena
 Cole. The record does not establish Hale's reason for rejecting the proposed warning.

 F038
 Hale's authenticated internal email is Record Exhibit PX-005.

 F039
 PX-005 is an admissible statement of a party opponent.

 F040
 PX-005 states that Apex would retain the shorter warning despite the engineering recommendation. PX-005
 does not state that the decision was made to avoid a per-unit cost increase and does not state any other reason
 for the decision.

 Preserved engineering recommendation
 F035: Apex safety engineer Elena Cole recommended a Zeta-9-specific warning, local-exhaust instruction, and
 respirator instruction before the MX-400 entered the market.

 F036: Cole's recommendation appears in PX-003.

 Preserved exclusion
 F051-F054 remain unchanged. Sam Reed lacked personal knowledge; his statement is inadmissible and may
 not support any element or damages finding. No substitute punitive evidence was added.

 Verification
 The separate verifier compares the complete variant with an independently specified allowed transformation of
 the hash-pinned reference input. It checks every unaffected fact and controlling rule, rather than trusting a
 stored PASS label.




Grounded DI LLC | New local evaluator | Closed-world evidence                                              Page 2
 2 / Controlling closed-world rules
 L007 / Negligent Failure to Warn
 Evidence that a manufacturer knowingly rejected a specific safety warning recommended by its engineering
 staff permits a reasonable jury to find breach.

 L010 / Punitive Damages
 Punitive damages may be submitted to the jury when clear and convincing admissible evidence would permit a
 finding that the defendant consciously disregarded a known substantial safety risk. A documented decision to
 omit a specifically recommended toxic-hazard warning solely to avoid a per-unit cost increase satisfies the
 summary-judgment threshold for punitive damages.

 L015 / Hearsay Exclusion
 An out-of-court statement offered for its truth by a declarant lacking personal knowledge is inadmissible unless
 another stated rule applies. No exception applies to Sam Reed's alleged statement.

 L001 / L008 / L018 - summary judgment and experts
 Admissible substantial-factor testimony supports submission to a jury. Competing admissible expert opinions
 remain a factual dispute; the evaluator does not weigh credibility or treat the dispute as a contradiction.

 L017 / L020 - instructions, readiness, and export
 Every surviving jury issue must map to the stipulated instructions. VerdictReady requires admissible relied-upon
 evidence, correct law and element mapping, supported damages, replay validation, no hard lock, and
 authorized export. Correctly granting punitive summary judgment is not a gate failure.

 Exact-case operationalization
 The original explicit cost-motive statement supplies the stipulated L010 predicate. In the altered record, no
 affirmative motive or substitute conscious-disregard evidence is supplied. Knowing rejection still supports
 negligence under L007; this evaluator does not infer an unstated punitive motive from it alone.

 L019 confines this synthetic benchmark to its supplied authorities. No actual-jurisdiction legal conclusions or outside authority
 validation are asserted.




Grounded DI LLC | New local evaluator | Closed-world evidence                                                                  Page 3
 3 / Expected and observed selectivity
 Each of the three measured runs matches the declared expected result. Exactly two disposition fields changed
 relative to the preserved original gate matrix.

   Disposition                        Original reference                        New - observed A/B/C

   Strict liability                   Deny summary judgment                     Deny summary judgment

   Negligence                         Deny summary judgment                     Deny summary judgment

   Compensatory damages               Deny summary judgment                     Deny summary judgment

   Punitive damages                   Deny summary judgment                     Grant summary judgment

   Overall motion                     DENIED                                    Granted in part / denied in part

   Sam Reed                           Excluded and not used                     Excluded and not used

   Jury instructions                  PASS                                      PASS

   Appellate review                   Not applicable                            Not applicable

   FilingReady                        Not applicable                            Not applicable

   VerdictReady                       YES                                       YES

   Export authorized                  True                                      True



 Surviving jury instructions
 conflicting expert testimony: MI-EVID-101; future medical expenses: MI-DAM-103; negligence: MI-NEG-101, MI-NEG-205; pain
 and suffering: MI-DAM-104; past lost wages: MI-DAM-102; past medical expenses: MI-DAM-101; product identification:
 MI-PL-101; specific causation: MI-CAUS-101; strict liability failure to warn: MI-PL-201, MI-PL-202, MI-PL-203

 MI-PUN-101 is not required because punitive damages does not survive for jury determination. All 14 declared major gate
 statuses match; LEGAL-KERNEL is NOT_ACTIVE and appellate review is NOT_APPLICABLE.




Grounded DI LLC | New local evaluator | Closed-world evidence                                                              Page 4
 4 / Complete five-hash ledger
 All three runs were created by separate processes from the same frozen input. These are the complete measured SHA-256
 values; none is truncated.

 Canonical input JSON
 Run-A: c53a77a0df2032fc2931bfb1793991d274c98ce1a6d2f7aef5534bc3ae0df561
 Run-B: c53a77a0df2032fc2931bfb1793991d274c98ce1a6d2f7aef5534bc3ae0df561
 Run-C: c53a77a0df2032fc2931bfb1793991d274c98ce1a6d2f7aef5534bc3ae0df561

 Normalized record CSV
 Run-A: 99aa74d84fe9e33cedaf9a4820eb846ce5618f0aa74e8951241ba1347ada93cc
 Run-B: 99aa74d84fe9e33cedaf9a4820eb846ce5618f0aa74e8951241ba1347ada93cc
 Run-C: 99aa74d84fe9e33cedaf9a4820eb846ce5618f0aa74e8951241ba1347ada93cc

 Gate matrix JSON
 Run-A: 242401fedf2c6a01b0cc376e8734cfeafff180f5d669ae9775e43a95c2014775
 Run-B: 242401fedf2c6a01b0cc376e8734cfeafff180f5d669ae9775e43a95c2014775
 Run-C: 242401fedf2c6a01b0cc376e8734cfeafff180f5d669ae9775e43a95c2014775

 Assessment TXT
 Run-A: 90faa90efa8f79aab956427479788e616f87b0178606d4f2563535cccd5a0378
 Run-B: 90faa90efa8f79aab956427479788e616f87b0178606d4f2563535cccd5a0378
 Run-C: 90faa90efa8f79aab956427479788e616f87b0178606d4f2563535cccd5a0378

 Canonical run ZIP
 Run-A: 947314014bd8251f8cfb67d080bd7244d648752e9532aee109b85cf5f836324c
 Run-B: 947314014bd8251f8cfb67d080bd7244d648752e9532aee109b85cf5f836324c
 Run-C: 947314014bd8251f8cfb67d080bd7244d648752e9532aee109b85cf5f836324c



   Artifact                                               Direct bytes A=B=C               Hashes A=B=C

   Canonical input JSON                                   PASS / 0 mismatches              PASS

   Normalized record CSV                                  PASS / 0 mismatches              PASS

   Gate matrix JSON                                       PASS / 0 mismatches              PASS

   Assessment TXT                                         PASS / 0 mismatches              PASS

   Canonical run ZIP                                      PASS / 0 mismatches              PASS


 Canonical ZIP: four records only; ZIP_STORED; lexicographic order; fixed 1980 timestamps and 0644 regular-file mode; no
 receipts, comments, or extra fields. Run receipts with process IDs and timestamps are outside it.




Grounded DI LLC | New local evaluator | Closed-world evidence                                                          Page 5
 5 / Invalid hearsay control and refusal
 The candidate attempts to preserve punitive damages by relying on F051: "I heard Apex always knew the
 machine was dangerous." It changes punitive damages back to DENY_SUMMARY_JUDGMENT and the
 overall motion back to DENIED.

 Separate verifier
 REFUSED, exit code 2. Failure: INADMISSIBLE_EVIDENCE_RELIANCE. Controlling exclusion: L015 /
 F051-F054 / L020. Failed evidentiary/readiness/export path: VB-D-EAUR, VERDICTREADY-GATE,
 EXPORT-GATE.

 Actual local export boundary
 The writer independently refuses inadmissible evidence reliance and a legal-disposition mismatch. It creates an
 isolated directory for inventory but never reaches its export-file opening branch.

   Observed field                                                 Measured value

   VerdictReady                                                   NO

   Export authorized                                              false

   Export files opened                                            0

   Bytes written                                                  0

   Final export output inventory                                  [] - empty

   Independent Python open-event audit                            [] - no export-path opens



 Additional controls
 Seven altered-copy tests were rejected: modified reference law, restored cost fact, wrong disposition, Reed in
 the reliance trace, missing assessment, forged receipt hash, and changed ZIP bytes. A forged
 wrong-disposition candidate without Reed was also refused at the writer.

 Changing the expected-outcome oracle did not change the evaluator's derived decision. Original reference outcomes were
 recalculated by the new evaluator for comparison, without executing an original engine.




Grounded DI LLC | New local evaluator | Closed-world evidence                                                             Page 6
 6 / Preserved reference evidence
 A / Original five files
 Repository: Grounded-DI/grounded-di-replay-certificate-registry. Folder: Verdictbridge_demo-2. All five complete files are copied
 unchanged and hash-checked.

 Pinned commit: 8472b48470b6c35a3ad2778f0819f36d4ddaef1b
 Run-2-01_canonical_input.json

 2e631eb0d2d81d6625ad73f286049ccc988dea8de31028880f774bf76a496042

 Run-2-02_normalized_record.csv

 0ccc7f002330baa8b482486fed0e17a1d73b4bd3c95372cc52bf172585ee1a97

 Run-2-03_gate_matrix.json

 3485237ad08fac0192e72873620b5207702687fd6efbb4d0949d6c0d5d2bd9a2

 Run-2-04_verdictbridge_assessment.txt

 e977081b390b42f74a6779a4ee32252afcd7aa58fb73def9d7181dda1163facd

 Run-2-run_receipt.json

 0882d41eef9dda1f9f097f609fce77edaf7629d508da34e6d0c532b312924044


 B / Newly implemented evaluator
 source/evaluator.py - finite exact-case semantics, computed dispositions, deterministic record generation, and an isolated
 cooperative writer. It is not the original VerdictBridge engine.

 77b6478482316496f72f54e028ca2bc9ba257ffc4f6adaba3a2b2a100bab837c

 C / Separate verifier
 source/verify.py - imports no evaluator code; checks facts, authorities, decisions, exclusion, gates, instructions, receipts, ZIP
 content, hashes, and direct bytes. Authored in the same task; no external certification.

 269a841dd093b2161e3d063404a1a4f5cd6f5e7ada16cbde5a39f79ce760b023

 D / Actual measured executions
 Distinct process IDs: 67016, 67017, 67018. Each run receipt binds its source/input hashes and preserves actual export activity.




Grounded DI LLC | New local evaluator | Closed-world evidence                                                                   Page 7
 7 / Final disposition and practical limits

 PASS - all required measured conditions satisfied
 The altered legal result matches the declaration. Punitive damages alone changes among the four requested
 claim outcomes; the overall motion changes accordingly. Unrelated outcomes remain stable. Sam Reed
 remains excluded, the invalid control is refused, and all five canonical layers match by both direct bytes and
 SHA-256 across the three fresh runs.

 Scope and limitations
 This is a newly implemented local evaluator for one stipulated synthetic case and its exact allowed variant. It is not native
 VerdictBridge reproduction or execution of an original engine.

 The verifier is a separate internal logic path, authored in the same task. The certificate is unsigned and locally issued; no
 external auditor attestation occurred.

 No model calls, live organizational approval service, real court filing, external facts, or actual-jurisdiction legal validation were
 used.

 The writer boundary covers this cooperative local harness. It does not intercept other writers or establish hostile-process
 resistance, application-wide enforcement, or production readiness.

 Matching finite executions establish repeatability of these canonical records and this pipeline. They do not prove universal model
 determinism or mathematical certainty about every future execution.

 The reported numeric error of zero denotes unchanged exact record values. Six-decimal gate coverage values describe
 stipulated-record conformance, not calibrated legal confidence.

 Reproduce and inspect
 python3 -B source/verify.py
 python3 -B source/acceptance.py
 python3 -B source/reproduce.py /path/to/new/folder
 shasum -a 256 -c SHA256SUMS.txt
 The complete package includes source, preserved references, all three run folders and receipts, invalid-control evidence,
 measured verification, this PDF, README, unsigned replay certificate, and checksum manifest. This public release preserves
 local execution evidence.




Grounded DI LLC | New local evaluator | Closed-world evidence                                                                       Page 8

~~~
