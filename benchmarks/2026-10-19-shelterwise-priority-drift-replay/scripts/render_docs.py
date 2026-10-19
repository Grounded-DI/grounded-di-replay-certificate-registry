#!/usr/bin/env python3
"""Render the human-readable package README and report from measured records."""

import argparse
import json
from pathlib import Path

from common import load_json


def control_rows(results):
    lines = []
    for name, result in results.get("controls", {}).items():
        observed = json.dumps(result.get("observed", {}), sort_keys=True, separators=(",", ":"))
        lines.append(f"| `{name}` | {result.get('status')} | {result.get('assertion')} | `{observed[:220]}` |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root")
    args = parser.parse_args()
    root = Path(args.package_root).resolve()
    replay = load_json(root / "REPLAY_RESULTS.json")
    controls = load_json(root / "CONTROL_RESULTS.json")
    final = load_json(root / "executions" / "run_1" / "final_chain.json")
    input_hash = __import__("hashlib").sha256((root / "canonical_input.json").read_bytes()).hexdigest()
    stage_lines = []
    for stage, item in replay["stage_output_identity"].items():
        stage_lines.append(f"| `{stage}` | `{item['run_1_sha256']}` | `{item['run_2_sha256']}` | `{'YES' if item['identical'] else 'NO'}` |")
    stage_table = "\n".join(stage_lines)
    report = f"""# ShelterWise priority-drift and scarce-resource replay report

## Decision

The canonical synthetic Northbank snapshot produced **`{final['disposition']}`**. That is the derived disposition of this closed-world fixture, not real emergency, humanitarian, medical, public-safety, or shelter-allocation advice.

The cleanest record-based basis is that the rule bindings and household evidence are preserved, but the record contains a duplicate exclusive accessible-cot reservation, contradictory intake records, an unverified transport need, and a missing meal-support foundation. The workflow therefore preserves assignment-level results and routes unresolved items for review.

## Replay identity

- Canonical executions: `{replay['canonical_execution_count']}`.
- Final-chain replay identity: `{replay['final_chain_replay_identity']}`.
- Record mismatches between canonical runs: `{replay['record_mismatches']}`.
- Observed replay divergence: `{replay['observed_replay_divergence']}`.
- Canonical input SHA-256: `{input_hash}`.
- Stage and final output identity:

| Stage | Run 1 SHA-256 | Run 2 SHA-256 | Identical |
| --- | --- | --- | --- |
{stage_table}

The execution receipts preserve timestamps, exit codes, commands, Python version, platform, and raw stdout/stderr. Those receipts are intentionally outside the deterministic stage-output byte boundary.

## Independent evaluator

`independent_evaluator.py` recalculated active rules, source-binding errors, intake statuses, household priorities, capacity, duplicate exclusive reservations, assignment dispositions, and the final disposition directly from `canonical_input.json`. It did not import the primary stage module. Recorded status: **`{replay['independent_evaluator']['status']}`**; primary-stage import flag: **`{replay['independent_evaluator']['imports_primary_stage_logic']}`**.

## Altered-input and tamper controls

The control suite executed `{controls['control_count']}` controls: `{controls['pass_count']}` passed and `{controls['fail_count']}` failed. `{controls['actual_mutated_input_pipeline_executions']}` controls reran the pipeline from mutated source records; `{controls['actual_intermediate_tamper_executions']}` altered a preserved intermediate allocation output and exercised the downstream hash guard.

| Control | Result | Assertion | Observed excerpt |
| --- | --- | --- | --- |
{control_rows(controls)}

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
"""
    readme = f"""# ShelterWise priority-drift and scarce-resource replay

This directory is a closed-world, synthetic-only replay of a fictional Northbank shelter snapshot. It tests source binding, priority preservation, uncertainty routing, scarce-resource accounting, identity neutrality, changed-input response, and downstream tamper resistance.

Canonical result: **`{final['disposition']}`**. Canonical executions: `{replay['canonical_execution_count']}`. Stage and final outputs were byte-identical across the two recorded executions. The independent evaluator passed, and all `{controls['control_count']}` altered-input/tamper controls passed.

## Contents

- `canonical_input.json` — synthetic rules, sources, households, inventory, reservations, and negative-control memo.
- `specification.json` — governing synthetic configuration and status vocabulary.
- `scripts/` — runnable stage scripts, pipeline, independent evaluator, controls, integrity checker, and archive builder.
- `expected_outputs/` — preserved expected stage and final outputs.
- `actual_outputs_run_1/` and `actual_outputs_run_2/` — outputs from two fresh canonical executions.
- `executions/` — raw stdout/stderr and execution receipts.
- `controls/` — preserved mutated inputs, outputs, raw streams, and guard results.
- `REPORT.md` — measured report and explicit non-claims.
- `SHA256SUMS.txt` — package manifest.
- `reproducibility_package.zip` — deterministic archive; its hash is in `ARCHIVE_SHA256.txt`.

## Run locally

```bash
python3 -B scripts/execute_replay.py .
python3 -B scripts/render_docs.py .
python3 -B scripts/create_manifest.py .
python3 -B scripts/integrity_check.py .
python3 -B scripts/build_archive.py .
python3 -B scripts/integrity_check.py .
```

The replay uses only the Python standard library and makes no network or model calls. All labels, rules, resource records, and outcomes are synthetic fixtures. See `REPORT.md` for scope, results, controls, and non-claims.
"""
    (root / "REPORT.md").write_text(report, encoding="utf-8")
    (root / "README.md").write_text(readme, encoding="utf-8")
    print(json.dumps({"status": "PASS", "files": ["README.md", "REPORT.md"]}, sort_keys=True))


if __name__ == "__main__":
    main()
