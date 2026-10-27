# Expiry and Policy: Fresh Replay — October 27, 2026

Grounded DI LLC · Mark S. Weinstein. This is a fresh internal replay of the existing synthetic expiry and policy demonstration, not a new runtime or independent third-party certification.

## Pinned input and frozen contract

Source repository commit: `23b06cb7ab40a3450256fe0ad0aa4005885cf4c7` ([source](../../2026-09-10-di2-expiry-policy-v1/source/README.md)). The source files were fetched at that commit. The synthetic cases and expected results were the existing published inputs. The following plan was frozen before the two runs:

# Frozen replay plan
Target: public expiry and policy replay at commit 23b06cb7ab40a3450256fe0ad0aa4005885cf4c7, synthetic inputs, Python standard library.
Two independent fresh copies of pinned source; on each run SHA256SUMS validation, verify.py and acceptance.py. Required: all checks exit 0, no skipped checks, registered 25 cases, 10 boundary checks and 6 altered-copy controls preserved by upstream acceptance; canonical evidence/replay-identity.json must exactly match pinned upstream and each other, SHA-256 08f6750447a0f923d1b175a436f9ef03f98d0b50b755b52e276aed05bb410fe8. Separate real-clock observations are outside canonical identity. Scope: replay existing source and historical fixed snapshots, not fresh model inference. Freeze this plan before execution. Any mismatch or unexecuted required check halts publication.

## Execution and results

Two separately copied directories were checked and run in separate processes. Environment: Python 3.12.14 on Linux x86_64, standard library. In each copy, the commands were `sha256sum -c SHA256SUMS.txt`, `python3 -B verify.py`, and `python3 -B acceptance.py`, in that order. Each exited zero. The verifier generated a fresh process, compared regenerated canonical bytes against the frozen reference and checked the separate project reference evaluator. Acceptance checked expected cases, boundaries, tamper controls, and a new real-clock scenario.

For each run: 25 case checks, 10 additional boundary checks, six altered-copy controls rejected, and a new real-clock expiry denial with zero write-open attempts. Both verifiers reported the expected SHA-256 `08f6750447a0f923d1b175a436f9ef03f98d0b50b755b52e276aed05bb410fe8`; the two stored canonical reference files were also directly byte-compared. The checksum listings and full verifier/acceptance observations are below. The fresh real-clock timestamps vary by design and are outside the canonical replay identity.

## Scope

This replays the fixed synthetic historical snapshots using the existing source and its project-authored reference checker. The checker shares the same specification and serialization utilities, so agreement is an internal cross-check. No model, live service, authenticated approval, external deployment, or third-party certification was tested. The unsigned records and hashes provide local consistency and identity, not authenticity or proof of universal determinism. The underlying expiry guarantee remains a sampled-time local check, not a guarantee against scheduler delay or an external-effect deadline.

## Execution records

```json
{
  "environment": {
    "architecture": "x86_64",
    "os": "Linux",
    "python": "3.12.14"
  },
  "runs": [
    {
      "acceptance": {
        "expected_case_checks": 25,
        "extra_boundary_checks": 10,
        "negative_controls": [
          {
            "reason": "FRESH_RUN_FAILED:{\"status\": \"FAIL\", \"reason\": \"APPROVAL_FAILED:valid\"}",
            "rejected": true,
            "test": "report"
          },
          {
            "reason": "REPLAY_IDENTITY_MISMATCH",
            "rejected": true,
            "test": "expiry_evidence"
          },
          {
            "reason": "REPLAY_IDENTITY_MISMATCH",
            "rejected": true,
            "test": "same_version_policy"
          },
          {
            "reason": "SAVED_EXPORT_MISMATCH",
            "rejected": true,
            "test": "saved_export"
          },
          {
            "reason": "SAVED_RESULTS_MISMATCH",
            "rejected": true,
            "test": "saved_decision"
          },
          {
            "reason": "REPLAY_IDENTITY_MISMATCH",
            "rejected": true,
            "test": "source_binding"
          }
        ],
        "new_real_clock_test": {
          "approval": {
            "decision": "ALLOW",
            "reason": "AUTHORIZED"
          },
          "clock": "OS wall clock via time.time_ns; Unix milliseconds",
          "execution": {
            "decision": "DENY",
            "execution_time": 1793124131083,
            "files": {},
            "reason": "EXPIRED",
            "write_open_attempts": 0
          },
          "wait_clock": "time.monotonic_ns",
          "wait_elapsed_ns": 252484596
        },
        "original_reverification": "PASS",
        "original_unchanged": true,
        "status": "PASS",
        "verification": {
          "canonical_bytes_identical": true,
          "case_count": 25,
          "fresh_process_execution": true,
          "real_clock_historical_replay": "PASS",
          "reference_comparison": "PASS",
          "replay_sha256": "08f6750447a0f923d1b175a436f9ef03f98d0b50b755b52e276aed05bb410fe8",
          "saved_exports": "PASS",
          "status": "PASS"
        }
      },
      "checksum_lines": [
        "PUBLICATION_NOTES.md: OK",
        "README.md: OK",
        "acceptance-results.json: OK",
        "acceptance.py: OK",
        "application-provenance.json: OK",
        "assistant-response.txt: OK",
        "cases.json: OK",
        "codec.py: OK",
        "evidence/exports/valid/approved/report.txt: OK",
        "evidence/exports/valid_again/approved/report.txt: OK",
        "evidence/replay-identity.json: OK",
        "evidence/replay-identity.sha256: OK",
        "evidence/results.json: OK",
        "failed-attempt-prompt.txt: OK",
        "kernel.py: OK",
        "negative-controls.json: OK",
        "real-clock-case.json: OK",
        "real-clock-observation.json: OK",
        "record.py: OK",
        "reference.py: OK",
        "replay-certificate.json: OK",
        "report.txt: OK",
        "run.py: OK",
        "submitted-prompt.txt: OK",
        "verification.json: OK",
        "verify.py: OK"
      ],
      "verify": {
        "canonical_bytes_identical": true,
        "case_count": 25,
        "fresh_process_execution": true,
        "real_clock_historical_replay": "PASS",
        "reference_comparison": "PASS",
        "replay_sha256": "08f6750447a0f923d1b175a436f9ef03f98d0b50b755b52e276aed05bb410fe8",
        "saved_exports": "PASS",
        "status": "PASS"
      }
    },
    {
      "acceptance": {
        "expected_case_checks": 25,
        "extra_boundary_checks": 10,
        "negative_controls": [
          {
            "reason": "FRESH_RUN_FAILED:{\"status\": \"FAIL\", \"reason\": \"APPROVAL_FAILED:valid\"}",
            "rejected": true,
            "test": "report"
          },
          {
            "reason": "REPLAY_IDENTITY_MISMATCH",
            "rejected": true,
            "test": "expiry_evidence"
          },
          {
            "reason": "REPLAY_IDENTITY_MISMATCH",
            "rejected": true,
            "test": "same_version_policy"
          },
          {
            "reason": "SAVED_EXPORT_MISMATCH",
            "rejected": true,
            "test": "saved_export"
          },
          {
            "reason": "SAVED_RESULTS_MISMATCH",
            "rejected": true,
            "test": "saved_decision"
          },
          {
            "reason": "REPLAY_IDENTITY_MISMATCH",
            "rejected": true,
            "test": "source_binding"
          }
        ],
        "new_real_clock_test": {
          "approval": {
            "decision": "ALLOW",
            "reason": "AUTHORIZED"
          },
          "clock": "OS wall clock via time.time_ns; Unix milliseconds",
          "execution": {
            "decision": "DENY",
            "execution_time": 1793124143110,
            "files": {},
            "reason": "EXPIRED",
            "write_open_attempts": 0
          },
          "wait_clock": "time.monotonic_ns",
          "wait_elapsed_ns": 252128927
        },
        "original_reverification": "PASS",
        "original_unchanged": true,
        "status": "PASS",
        "verification": {
          "canonical_bytes_identical": true,
          "case_count": 25,
          "fresh_process_execution": true,
          "real_clock_historical_replay": "PASS",
          "reference_comparison": "PASS",
          "replay_sha256": "08f6750447a0f923d1b175a436f9ef03f98d0b50b755b52e276aed05bb410fe8",
          "saved_exports": "PASS",
          "status": "PASS"
        }
      },
      "checksum_lines": [
        "PUBLICATION_NOTES.md: OK",
        "README.md: OK",
        "acceptance-results.json: OK",
        "acceptance.py: OK",
        "application-provenance.json: OK",
        "assistant-response.txt: OK",
        "cases.json: OK",
        "codec.py: OK",
        "evidence/exports/valid/approved/report.txt: OK",
        "evidence/exports/valid_again/approved/report.txt: OK",
        "evidence/replay-identity.json: OK",
        "evidence/replay-identity.sha256: OK",
        "evidence/results.json: OK",
        "failed-attempt-prompt.txt: OK",
        "kernel.py: OK",
        "negative-controls.json: OK",
        "real-clock-case.json: OK",
        "real-clock-observation.json: OK",
        "record.py: OK",
        "reference.py: OK",
        "replay-certificate.json: OK",
        "report.txt: OK",
        "run.py: OK",
        "submitted-prompt.txt: OK",
        "verification.json: OK",
        "verify.py: OK"
      ],
      "verify": {
        "canonical_bytes_identical": true,
        "case_count": 25,
        "fresh_process_execution": true,
        "real_clock_historical_replay": "PASS",
        "reference_comparison": "PASS",
        "replay_sha256": "08f6750447a0f923d1b175a436f9ef03f98d0b50b755b52e276aed05bb410fe8",
        "saved_exports": "PASS",
        "status": "PASS"
      }
    }
  ]
}
```
