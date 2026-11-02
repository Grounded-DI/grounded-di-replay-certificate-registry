# NIST water — temperature-dependent seven-boundary replay

## Source

The NIST Chemistry WebBook, SRD 69, Water, liquid-phase heat-capacity Shomate equation, provides coefficients A = -203.6060, B = 1523.290, C = -3196.413, D = 2474.455, E = 3.855326 for 298–500 K and Cp in J/(mol*K), with t = T/1000. The source's 298 K table row gives 75.38 J/(mol*K). It cites Chase, 1998, NIST-JANAF Thermochemical Tables, Fourth Edition: https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=3&Table=on&Type=JANAFL . The selected table does not numerically state pressure or uncertainty. NIST states its data compilation is copyrighted; `source_extract.txt` is a short attributed project transcription, not original HTTP bytes, an official signed source, or a redistribution of the full database.

## Calculation

For a synthetic one mole warmed from 298 to 300 K, integrate Cp(T) = A + B*t + C*t² + D*t³ + E/t². Since T = 1000*t, Q = n*1000*[A*t + B*t²/2 + C*t³/3 + D*t⁴/4 - E/t] between endpoints. All specified decimal coefficients are represented exactly as rational numbers. Integrated heat is approximately 150.727448729312 J. A constant-Cp comparison uses the rounded 298 K table value, 75.38 J/(mol*K), and gives 150.76 J. Integrated minus constant is approximately -0.032551270688 J. These decimal presentations are rounded; canonical outputs contain exact rational strings, not floating-point approximations. Values have the limits of the displayed, rounded source coefficients and table value; the source does not supply numerical uncertainty on this table row. The model presumes liquid water and no heat loss or phase change. It is not an experimental measurement or universal physical prediction.

## Replay

The source record, fixture, expected artifact hashes, equations and controls were frozen before execution. `freeze_reference.py` documents fixture construction and would overwrite frozen files; do not run it as a replay. Seven boundaries are source, validation, normalized inputs, endpoint heat capacities, integral, approximation comparison, and commitment to the first six. The commitment is not an independent scientific finding.

Requires Python 3 and its standard library. Run in new nonexistent directories:

```sh
sha256sum -c SHA256SUMS.txt
python3 -B pipeline.py --out /tmp/nist_run1
python3 -B pipeline.py --out /tmp/nist_run2
python3 -B checker.py --out /tmp/nist_run1
python3 -B checker.py --out /tmp/nist_run2
python3 -B controls.py
```

Both original runs matched seven frozen expected hashes and were directly byte-compared. See `execution/comparisons.json`, `execution/commands.json`, logs and environment. The separately implemented checker uses a factorized algebraic form of the integral, does not import the pipeline, and checks endpoints, heat, approximation, frozen bindings, artifact hashes, and commitment. It shares the source record, formula assumptions, Python Fraction and SHA-256 libraries, and host. It is project-local, not unaffiliated review.

## Controls and limits

Nine registered controls passed with zero failures, errors, or skips. `execution/controls.stdout` records each changed input, expectation, observed result and assertion: changed coefficient, out-of-range temperature, reversed or missing bounds, unit substitutions, a valid changed amount, altered endpoint handoff, and wrong heat with recalculated commitment. Changed amount is correctly computed but rejected as a different frozen fixture; it is not called a bad scientific input. Endpoint handoff is checked against a value recomputed in the same local process, not authenticated as an external sensor. Matching an unsigned project-authored source record to itself does not independently establish source authenticity. No production, experimental, or universal model-determinism claim is made.
