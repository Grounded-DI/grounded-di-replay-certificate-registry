# Integrated Legal Evidence Chain Replay

This is a **local-only, closed-world replay package** for one synthetic
product-liability matter. It connects four stage implementations:

1. **BriefWise** — authority and proposition binding;
2. **DepoBot** — source-linked testimony tracing;
3. **PIDBot** — product and exposure evidence separation; and
4. **VerdictBridge** — guarded litigation-sufficiency synthesis.

Every authority, witness, transcript entry, exhibit, product, entity, worksite,
and outcome is a synthetic fixture. The package makes no real legal, medical,
product, exposure, dose, causation, liability, filing-readiness, external-
verification, or production-deployment claim.

## Local-only status

The repository URL in the surrounding task is context only. This package was
created in an existing local checkout. No repository, branch, commit, push,
pull request, publication, or other remote write was performed. The repository
root `README.md` was inspected and left unchanged.

## Quick replay

From this directory:

```bash
python3 -B run_chain.py input.json run_1
python3 -B run_chain.py input.json run_2
python3 -B independent_evaluator.py
python3 -B chain_controls.py
sha256sum -c SHA256SUMS.txt
```

The scripts use only the Python standard library and make no network or model
calls. Each chain run starts four fresh subprocesses and writes raw stdout,
stderr, execution receipts, stage JSON, and the final chain JSON to its run
directory.

## Matter and stage boundaries

The fixture defines a synthetic Commonwealth summary-judgment posture involving
an alleged Model Z-14 pump gasket at North Plant in 2014. The fixture includes
three synthetic authorities, a complaint, seven source-linked transcript
entries, three synthetic exhibits, product/manufacturer references, component
and material assertions, exposure allegations, a missing dose record, and a
missing causation opinion.

The boundary is explicit:

```text
product identification ≠ component identification ≠ material content
≠ exposure ≠ dose ≠ causation ≠ legal liability
```

`stage_specs/` contains separate specifications for each stage. The stage
outputs preserve the source fields needed to inspect the chain rather than
collapsing them into a single conclusion.

## Recorded result

The two fresh runs produced identical canonical stage records and final-chain
records. The independent evaluator passed. The final synthetic disposition is
`INSUFFICIENT` because the closed-world record contains unresolved authority
binding, a source-linked testimony contradiction, unresolved material/exposure,
dose, and causation evidence, and an unsupported complete-liability assertion.
The cleanest synthetic recommendation is to reserve a final sufficiency
ruling pending the identified gaps.

This is a measured result of this fixture and these scripts. It is not a legal
conclusion about any real matter.

## Controls

`chain_controls.py` records each altered-input result and verifies that the
chain changes or refuses the alteration when:

- an authority is removed;
- a deposition answer is changed;
- a transcript page/line binding is changed;
- a product identifier is replaced;
- unsupported material evidence is added;
- a causation override is injected;
- an intermediate stage record is altered after downstream generation; or
- the final chain is manually changed to `VERDICT_READY`.

The DepoBot output also preserves a negative control: Witness B's lack of
observation and inability to identify the repairer are not classified as a
contradiction.

## Files

- `input.json` — canonical synthetic matter;
- `stage_specs/` — separate stage specifications;
- `briefwise.py`, `depobot.py`, `pidbot.py`, `verdictbridge.py` — runnable stage scripts;
- `run_chain.py` — fresh subprocess chain runner;
- `independent_evaluator.py` — separate end-to-end verifier that does not import stage logic;
- `chain_controls.py` — altered-input and downstream-injection controls;
- `expected_stage_outputs/` and `expected_final_chain.json` — expected canonical results;
- `run_1/` and `run_2/` — fresh run receipts, raw stdout/stderr, and outputs;
- `replay_summary.json`, `negative_control_results.json`, and `environment.json` — recorded results and environment;
- `REPORT.md` — human-readable measured report;
- `SHA256SUMS.txt` — file hashes;
- `reproducibility_package.tar.gz` — local reproducibility archive, with its hash in the adjacent `.sha256` file.

The proposed commit message and description are retained only in the task
prompt; no commit was created.
