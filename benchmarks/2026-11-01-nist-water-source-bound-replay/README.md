# Source-bound water heat-capacity replay

## Source and provenance

The source is the National Institute of Standards and Technology, NIST Chemistry WebBook, SRD 69, **Water**, liquid phase heat capacity (Shomate equation), table row at 298 K: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=3&Table=on&Type=JANAFL . The table lists 75.38 J/(mol·K) at 298 K; its source reference is Chase, 1998, NIST-JANAF Thermochemical Tables, Fourth Edition, and the page says the data were last reviewed in March 1979. The table is generated from the displayed Shomate representation, not an observed experiment in this project. The selected row states neither numerical uncertainty nor numerical pressure; neither is supplied by this demonstration. The page describes liquid-phase constant-pressure heat capacity and a 298–500 K representation range.

NIST displays molecular weight 18.0153 for water; this fixture interprets that value as a molar mass of 18.0153 g/mol. `source_record.json` identifies the material, value, conditions, reference, URL, retrieval date (2026-11-01), and limitations. `source_extract.txt` is a short, manually transcribed data extract with its own SHA-256, not original HTTP bytes, a digital signature, or a NIST attestation of this package. The public page states that the compilation is copyrighted and governed by the Standard Reference Data Act. No right to redistribute the full database is claimed.

## Fixture and result

The assumed mass is 18.0153 g and the assumed delivered heat is 0.07538 kJ. With the fixture's molar-mass interpretation, that is exactly 1 mol. The code converts heat to 75.38 J and applies Q = n Cp ΔT using the rounded source-table value as an exact rational input. Holding Cp constant, the calculated temperature change is 1 K. The result is a modeled approximation for a small change from 298 K, not an exact measurement or a claim that Cp stays constant with temperature. The model assumes no losses and no phase change; the source does not validate these assumptions or the synthetic mass and heat.

## Replay

The source record, fixture, expected hashes, equations, control outcomes, and canonical serialization were frozen before the pipeline ran. `freeze_reference.py` is retained as provenance; it overwrites the frozen files and is not a replay command. Two fresh local processes produced all seven artifacts byte-identical and matching their predeclared expected hashes. `execution/comparisons.json` records all hashes and direct byte comparisons.

The independently written checker recalculates the result and J/kJ conversion from the source-bound inputs without importing the pipeline. It also compares the source record, fixture, and outputs to frozen identities and checks the commitment. It shares the fixture, scientific assumptions, Python Fraction and SHA-256 libraries, and host. Matching an unsigned, project-authored source record to itself does not independently authenticate NIST or prove scientific correctness. The seventh boundary commits to the other six; it is not a separate scientific result.

Requires Python 3 and its standard library. From this directory, use paths that do not already exist:

```sh
sha256sum -c SHA256SUMS.txt
python3 -B pipeline.py --out /tmp/water_A
python3 -B pipeline.py --out /tmp/water_B
python3 -B checker.py --out /tmp/water_A
python3 -B checker.py --out /tmp/water_B
python3 -B controls.py
```

Compare all seven corresponding files directly and to `expected_hashes.json`. The checker is a fixed-fixture verifier; it intentionally rejects legitimate changed inputs as non-baseline even where their recomputed arithmetic is correct.

## Tests and limitations

Nine registered controls were executed and passed, with zero failures, errors, and skips. `execution/controls.stdout` records each change, expected outcome, actual observation, exit code, and assertion. Wrong material, altered source value, changed or missing source conditions, changed unit, and missing source reference are rejected. Doubling mass gives a valid 1/2 K calculation but the frozen replay checker rejects it as a different fixture. An altered quantity handoff is rejected before output. A coherent wrong result with a recalculated commitment is still rejected by the separate calculation and frozen hashes.

The intermediate handoff is compared with a value recomputed within the same process; it is not a signed external measurement. The data shown are a limited table extract, not a complete independently verified NIST data distribution. There is no claim of actual reaction behavior, universal model determinism, experimental validation, production readiness, or external certification.
