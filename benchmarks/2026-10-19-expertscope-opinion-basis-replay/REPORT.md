# ExpertScope — Opinion-Basis and Causation-Boundary Replay

## Scope

Closed-world synthetic product-liability fixture. Every expert, source, person, entity, product, medical fact, measurement, method, and outcome is synthetic. No real authority is used.

## Measured replay

- Canonical executions: 2
- Four stages per execution: SourceBinder, OpinionMapper, CausationBoundary, VerdictBridge
- Stage and final output identity: PASS
- Stage executions: 8 total; 8 pass, 0 fail
- Record mismatches across canonical runs: 0
- Observed replay divergence: 0
- Independent evaluator: PASS
- Source bindings: PASS; unresolved/mismatched bindings: 0
- Opinion results: {"QUALIFIED": 1, "SUPPORTED": 1, "UNRESOLVED": 0, "UNSUPPORTED": 1}
- Final unresolved dimensions: 7
- Boundary result: INSUFFICIENT
- Final disposition: INSUFFICIENT
- Final chain SHA-256: 770d6e776d5bd3b282f94f65a38844bf01e4d0b20ded50064085f23fbb28d426
- Altered and negative controls: PASS (8/8 passed)

## Stage hashes

| Stage | SHA-256 |
|---|---|
| SourceBinder | 9ea3301f045b3496b440e517ea6888ca2adfc0e0530d37d353a6e2db36de9468 |
| OpinionMapper | dc8c88a0bcaf93d556d2b1401e34c1e14973b5f31d15c013b501acb80357e58d |
| CausationBoundary | 48284ea056ce5c79004d68d036884b18e1686aef24dce3921be94535c304718e |
| VerdictBridge | 770d6e776d5bd3b282f94f65a38844bf01e4d0b20ded50064085f23fbb28d426 |

## Result

The synthetic diagnosis description is supported by the supplied synthetic medical summary. The conditional medical causation opinion remains qualified by unsupported or unresolved material, exposure, dose, and alternative-cause assumptions. The dose characterization is unsupported because the expert disclaims a calculation and the fixture supplies no quantitative measurement. Product identity is supported only at the pump/manufacturer level; component linkage remains unresolved. Material content and dose are missing. Legal causation and liability remain unresolved. The final result is **INSUFFICIENT** with a reserve-for-record-development assessment.

An altered record adding a synthetic service log, component test, and task measurement changes the result from INSUFFICIENT to REVIEW_REQUIRED. The added records support specified links but do not decide legal causation or liability. A conclusory assertion alone leaves dose missing.

## Integrity and limitations

Two canonical runs matched across all four stage outputs and final output. Independent evaluator logic is in a separate file and imports none of the primary stage scripts. Hashes establish byte/content identity under the stated serialization; they do not prove source truth or substantive correctness.

This package does not establish real legal correctness, admissibility, clinical validity, real-world product identification, exposure, dose, medical causation, legal causation, liability, filing readiness, independent fresh-generation provenance, external verification, or deployment.

## Reproduction

Run the commands in `commands.txt` from this directory. Python version and platform are preserved in each run's `execution.json`; timestamps are UTC.
