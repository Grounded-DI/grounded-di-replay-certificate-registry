# DepoBot — Testimony-Contradiction Replay

## Scope

This is a closed-world synthetic replay package. The records, authorities, transcript, products, entities, and outcomes are test fixtures. They do not represent real legal authorities, testimony, products, people, worksites, medical conclusions, or legal results.

## Measured execution

- Canonical executions: 2
- Canonical output identity: PASS
- Canonical record SHA-256: `2020e012f9010b6bef2ffd73d722d8528b54d1ff6545654ded406c04e7188f4a`
- Independent verifier: PASS
- Altered-record/tamper controls: PASS
- External verification: UNVERIFIED

## Evidence boundary

The package establishes only the recorded rule-governed behavior for this fixed input, specification, source, and environment. It does not establish universal model determinism, independent fresh-generation provenance, legal correctness, filing readiness, real-world exposure or causation, or production deployment.

## Reproduction

```bash
python3 -B replay.py
python3 -B verifier.py
python3 -B tamper_controls.py
```
