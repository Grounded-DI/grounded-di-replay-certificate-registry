# ShelterWise priority-drift and scarce-resource replay report

## Decision

The canonical synthetic Northbank snapshot produced **`REVIEW_REQUIRED`**. That is the derived disposition of this closed-world fixture, not real emergency, humanitarian, medical, public-safety, or shelter-allocation advice.

The cleanest record-based basis is that the rule bindings and household evidence are preserved, but the record contains a duplicate exclusive accessible-cot reservation, contradictory intake records, an unverified transport need, and a missing meal-support foundation. The workflow therefore preserves assignment-level results and routes unresolved items for review.

## Replay identity

- Canonical executions: `2`.
- Final-chain replay identity: `True`.
- Record mismatches between canonical runs: `[]`.
- Observed replay divergence: `False`.
- Canonical input SHA-256: `882f25b14be9edfbd55d1fbd7bb7fe6960c068aa43723023238fea58e6848569`.
- Stage and final output identity:

| Stage | Run 1 SHA-256 | Run 2 SHA-256 | Identical |
| --- | --- | --- | --- |
| `allocationbridge` | `c6237abf5099ebe40ace4715cac296b7f6dd187891f1061e8b72f3a8a21a5f87` | `c6237abf5099ebe40ace4715cac296b7f6dd187891f1061e8b72f3a8a21a5f87` | `YES` |
| `capacityledger` | `241f29c2cb44d3b22eeea177d74d09d173bf4b9fc5b57cbc593f672af53c31b9` | `241f29c2cb44d3b22eeea177d74d09d173bf4b9fc5b57cbc593f672af53c31b9` | `YES` |
| `driftshield` | `d50fe1fe0e0e6581bd694b9cb75f280396f235fefc5e05b2b842ae254549cf09` | `d50fe1fe0e0e6581bd694b9cb75f280396f235fefc5e05b2b842ae254549cf09` | `YES` |
| `final_chain` | `3e3d4f94d71759ab8eff99fbd93e5e718f0089bc7b78ec10848daf792d740cb5` | `3e3d4f94d71759ab8eff99fbd93e5e718f0089bc7b78ec10848daf792d740cb5` | `YES` |
| `intakebinder` | `48d684c571eeab1d55153928aef93caaeec25bed7b0bf4712db442c1c0b21604` | `48d684c571eeab1d55153928aef93caaeec25bed7b0bf4712db442c1c0b21604` | `YES` |
| `rulebinder` | `65ba5ea6f4b9765ff08521382b1a2af470d8ad6171accd5dd4c6205591b25b4a` | `65ba5ea6f4b9765ff08521382b1a2af470d8ad6171accd5dd4c6205591b25b4a` | `YES` |

The execution receipts preserve timestamps, exit codes, commands, Python version, platform, and raw stdout/stderr. Those receipts are intentionally outside the deterministic stage-output byte boundary.

## Independent evaluator

`independent_evaluator.py` recalculated active rules, source-binding errors, intake statuses, household priorities, capacity, duplicate exclusive reservations, assignment dispositions, and the final disposition directly from `canonical_input.json`. It did not import the primary stage module. Recorded status: **`PASS`**; primary-stage import flag: **`False`**.

## Altered-input and tamper controls

The control suite executed `16` controls: `16` passed and `0` failed. `15` controls reran the pipeline from mutated source records; `1` altered a preserved intermediate allocation output and exercised the downstream hash guard.

| Control | Result | Assertion | Observed excerpt |
| --- | --- | --- | --- |
| `accessibility_need_removed` | PASS | removed accessibility evidence became missing | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `capacity_reduced_below_demand` | PASS | cot demand exceeded altered capacity | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `conclusory_assertion_only` | PASS | conclusory memo did not establish a need | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `confirmed_safety_to_unverified` | PASS | confirmed safety downgrade changed priority and assignment | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":6},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"UNVERIFIED","missing_f` |
| `downstream_assignment_injection` | PASS | injected downstream assignment was ignored and flagged | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `duplicate_household` | PASS | duplicate household candidate preserved | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `duplicate_resource_reservation` | PASS | duplicate reservation produced a capacity conflict | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":["DUPLICATE_OR_OVERALLOCATED:COT-STD-001"],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"` |
| `intermediate_allocation_tamper` | PASS | downstream hash guard rejects altered allocation output | `"{\"expected_hash\": \"c707d005230f207525891d8721891d1bbfde6df4c273764d05f1895e89521f33\", \"observed_hash\": \"03d029c86866fb398ddb2b9bfad41ef651b3c1241b4bca82206de6ce300666de\", \"status\": \"REJECTED\"}"` |
| `labels_permuted` | PASS | display labels did not affect decisions | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `missing_evidence_collapse` | PASS | existing unverified record could not silently become confirmed | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `negative_control_memo_altered` | PASS | altered negative-control memo did not affect allocation | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `priority_inversion` | PASS | priority inversion was detected from source mismatch | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":7},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `stale_record_newer_without_matching_authority` | PASS | unauthorized rule did not enter active rule set | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `supporting_new_confirmation` | PASS | new source-supported confirmation changed H-004 to assignable | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `unauthorized_priority_rule_added` | PASS | unauthorized rule did not enter active rule set | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |
| `unsupported_confirmation` | PASS | status-only confirmation was rejected | `{"allocation":[{"assignments":[{"accessible":false,"conflicts":[],"controlling_rule":{"need_type":"immediate_safety","priority_level":1},"evidence_record_ids":["INT-H001-SAFETY"],"evidence_status":"CONFIRMED","missing_fo` |

The suite includes negative-control memo alteration and label permutation controls, a genuinely source-supported transport confirmation, a conclusory assertion without an authorized intake source, capacity reduction, duplicate household and reservation changes, unauthorized/stale rule changes, priority inversion, unsupported confirmation, missing-evidence collapse, downstream assignment injection, and intermediate-output tampering.

## What this evidence supports

- The disclosed synthetic rules are bound to source identifiers, locations, exact fragments, effective dates, and priority levels.
- Intake records preserve speaker/source, timestamp, exact fragment, status, contradiction, and missing/unverified states.
- Capacity is calculated from inventory and reservation records; the accessible cot over-allocation is detected without treating a multi-unit meal pool as an exclusive object.
- Household names and display labels do not alter the measured allocation output under the supplied identity-neutrality rule.
- A new source-supported confirmation changes H-004 from review to assignable, while a conclusory memo does not.
- Changing a source record, rule priority, reservation, capacity, or intermediate output changes or rejects the result as recorded by the controls.

## What this evidence does not support

This package does not establish real shelter operations, humanitarian suitability, medical or public-safety guidance, real-person or real-place identification, legal correctness, operational readiness, fairness outside the disclosed fixture, independent fresh-generation provenance, external verification, or production deployment. It is not a recommendation or an allocation decision for any real household.

## Reproduction

```bash
python3 -B scripts/execute_replay.py .
python3 -B scripts/render_docs.py .
python3 -B scripts/create_manifest.py .
python3 -B scripts/integrity_check.py .
python3 -B scripts/build_archive.py .
python3 -B scripts/integrity_check.py .
```

`SHA256SUMS.txt` covers the package files except the manifest itself, the ZIP archive, and the archive-hash sidecar. `ARCHIVE_SHA256.txt` records the SHA-256 of the deterministic ZIP produced after the manifest check. No remote or network call is used by the replay.

## Limitations

All records, rules, identities, capacities, reservations, outcomes, and controls are synthetic fixtures. No source beyond the preserved package is consulted. The result is reproducible under the disclosed code, input, specification, and serialization conditions; it is not a claim about arbitrary models, real-world drift, or real emergency decisions.
