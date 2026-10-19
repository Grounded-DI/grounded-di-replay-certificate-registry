# FastPath_5_6_Instant_Day_One_Canonical_Replay_Certificate

- Source PDF: [FastPath_5_6_Instant_Day_One_Canonical_Replay_Certificate.pdf](https://github.com/Grounded-DI/grounded-di-replay-certificate-registry/blob/main/FastPath_5_6_Instant_Day_One_Canonical_Replay_Certificate.pdf)
- Source Git blob SHA: `238187afa7ff8d3a5d917515a36b5c9de193857a`
- Source SHA-256: `e9991ec308f1d93480b989b38b694e8ac414de02bc9a56cf307bb51ad8830d64`
- Page count: 1
- Byte size: 3790
- Extraction method: `pdftotext -layout` (Poppler)
- Classification: `TEXT-EXTRACTABLE` in the Phase 1 inventory

Provenance: This is a derived machine-readable companion. The original PDF is unchanged. The text below is the direct `pdftotext -layout` output; no OCR, summarization, rewriting, or silent correction was applied. Literal form-feed page separators from the extractor output are retained.

## Raw extracted text

~~~text
                                         FASTPATH 5.6 INSTANT
                                       DAY-ONE CANONICAL REPLAY CERTIFICATE

TEST                                               TEST TYPE                                         EXECUTIONS
Canonical Replay Test 1                            controlled_speed_branch_replay                    3


RECORD MISMATCHES                                  HASH MISMATCHES                                   OBSERVED REPLAY DIVERGENCE
0                                                  0                                                 0


Independent Verification
The sealed JSON was parsed and canonically serialized using UTF-8, lexicographically sorted object keys, ensure_ascii = false, separators
(",",":"), no indentation, no BOM, and no leading/trailing whitespace or trailing newline. The independently recomputed SHA-256 matches all
three reported executions.

Canonical Record Actually Hashed
{"baseline_id":"R9-BASE-001","branch_id":"R9-CHG-001","comparative_fault_baseline":0.05,"comparative_fault_branch":0.1,"expected_branch_adjust
ed_high":1675800,"expected_branch_adjusted_low":1098900,"gross_high":1862000,"gross_low":1221000,"parent_id":"R9-BASE-001","protected_baseline
_adjusted_high":1768900,"protected_baseline_adjusted_low":1159950,"test_type":"controlled_speed_branch_replay"}

Verified SHA-256
84ab1d149c18715b4f2c3646ab6469f00ea453770f7a0ff94738d42310b55f9d

Execution        SHA-256                                                                                                             Result

      1          84ab1d149c18715b4f2c3646ab6469f00ea453770f7a0ff94738d42310b55f9d                                                       MATCH

      2          84ab1d149c18715b4f2c3646ab6469f00ea453770f7a0ff94738d42310b55f9d                                                       MATCH

      3          84ab1d149c18715b4f2c3646ab6469f00ea453770f7a0ff94738d42310b55f9d                                                       MATCH




                                        CERTIFIED RESULT
                      FASTPATH 5.6 INSTANT — CANONICAL REPLAY TEST 1: PASS

THREE EXECUTIONS                                                                             MATCH

CANONICAL RECORD IDENTITY                                                                    CONFIRMED

SHA-256 IDENTITY                                                                             CONFIRMED


Finding
“Three FastPath 5.6 Instant executions produced the same canonical serialization and the same SHA-256 digest for the sealed test input.”

Scope Limitation
“This result establishes replay identity for this specific sealed test and the three documented executions. It does not establish universal
determinism for other inputs, prompts, tools, environments, or runtime conditions.”

~~~
