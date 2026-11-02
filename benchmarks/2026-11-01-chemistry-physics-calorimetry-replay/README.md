# Chemistry-to-physics linked seven-boundary replay

A fictional fixture assumes 2 mol of material releases 40 kJ/mol, one quarter of that energy heats 2 kg of water, and the assumed heat capacity is 4,000 J/(kg·K). Exact rational arithmetic gives 80,000 J total energy, 20,000 J transferred, and a 5/2 K (2.5 K) temperature increase. All values are hypothetical inputs or results of the stated arithmetic, not measurements or a reaction procedure.

## Frozen scope and records

`CONTRACT.json`, `fixture.json`, and `expected_hashes.json` were written before the pipeline was executed. `freeze_reference.py` is the historical setup script; it writes frozen files and is included for provenance, not for normal replay. The canonical sequence is normalized inputs, moles, chemical energy, transferred energy, temperature change, checks, and SHA-256 commitment to those six files. The seventh is not an independent result. JSON is UTF-8 with sorted keys, ASCII escaping, compact separators, and a final LF; exact rational numbers are reduced strings.

Two separate local Python processes produced byte-identical files matching all seven frozen expected hashes. `execution/comparisons.json` records direct byte comparisons and hashes. `execution/commands.json`, raw output logs, and `execution/environment.json` document the run.

## Replay

Requires Python 3 and its standard library. From this directory, use new paths:

```sh
sha256sum -c SHA256SUMS.txt
python3 -B pipeline.py --out /tmp/calorimetry_A
python3 -B pipeline.py --out /tmp/calorimetry_B
python3 -B checker.py --out /tmp/calorimetry_A
python3 -B checker.py --out /tmp/calorimetry_B
python3 -B controls.py
```

Compare the two output directories directly and with `expected_hashes.json`. `checker.py` independently recalculates the key results from source inputs and explicitly performs the 1,000 J/kJ conversion, without importing the pipeline. It shares the fixture, equations, Python Fraction and SHA-256 libraries, and host. A passing check is project-local evidence, not independent external scientific certification.

## Controls and boundaries

Nine registered controls passed with zero failures, errors, or skips. `execution/controls.stdout` contains each change, expected disposition, observed result, process exit, and assertion. Changed amount and energy are valid computations that the frozen-fixture checker rejects as different fixtures. Unit mismatch, out-of-range capture, zero mass, zero heat capacity, and missing unit return controlled rejection before output. A changed chemistry handoff is rejected before transfer. A wrong temperature with a recalculated commitment retains internal commitment consistency but is rejected by mathematical and frozen-hash checks.

The handoff check compares a supplied record to chemistry recomputed inside the same local process. It does not authenticate an external sensor or protect against a hostile host. Temperatures are idealized: no vessel losses, varying heat capacity, phase changes, or reaction kinetics are modeled. No universal model determinism, clinical conclusion, actual experimental result, or real-world safety guarantee is claimed.
