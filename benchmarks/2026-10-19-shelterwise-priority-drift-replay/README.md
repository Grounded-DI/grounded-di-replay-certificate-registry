# ShelterWise priority-drift and scarce-resource replay

This directory is a closed-world, synthetic-only replay of a fictional Northbank shelter snapshot. It tests source binding, priority preservation, uncertainty routing, scarce-resource accounting, identity neutrality, changed-input response, and downstream tamper resistance.

Canonical result: **`REVIEW_REQUIRED`**. Canonical executions: `2`. Stage and final outputs were byte-identical across the two recorded executions. The independent evaluator passed, and all `16` altered-input/tamper controls passed.

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
