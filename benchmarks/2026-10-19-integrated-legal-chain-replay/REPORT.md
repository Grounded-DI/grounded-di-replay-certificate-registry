# Integrated Legal Evidence Chain Replay

## Scope

This package is one connected, closed-world synthetic product-liability matter. Synthetic authorities, transcript entries, exhibits, products, entities, worksite facts, and outcomes are test fixtures.

## Measured chain

- BriefWise authority binding: PASS
- DepoBot testimony trace: PASS
- PIDBot product/exposure separation: PASS
- VerdictBridge synthesis: PASS
- Fresh chain executions: 2
- Stage-level replay identity: PASS
- Final-chain replay identity: PASS
- Independent evaluator: PASS
- Negative controls: PASS
- Altered-stage/downstream-injection controls: PASS
- Final disposition: `INSUFFICIENT`
- VerdictReady: `false`
- Final chain SHA-256: `4b30e1074180b6319114e6279dfccf9160f53eb33d0c79a912e35ec052c13a14`

## Stage hashes

| Stage | Canonical SHA-256 |
|---|---|
| BriefWise | `860e5be6e001fcdf6218d54ff8c2c21b4dce4d50b30e2266ffcf12912828858f` |
| DepoBot | `2ad954f46c0fa1ed1357506c31987c39af120d3f0b35994d1e3179c716d546e6` |
| PIDBot | `21709fc5f41f3ff5637272b33b521f224de37c7a6d69cc756f90522295795de1` |
| VerdictBridge final chain | `4b30e1074180b6319114e6279dfccf9160f53eb33d0c79a912e35ec052c13a14` |

## Chain result

The product identity is bounded by a shared synthetic product/manufacturer reference. The testimony contains a recorded direct contradiction. Component identity remains under review. Material content is uncertain, exposure remains under review, dose is unquantified, and causation is unresolved. VerdictBridge therefore preserves the uncertainty and returns `INSUFFICIENT`; the motion recommendation is to reserve rather than manufacture a final liability or causation result.

## Controls

The control suite removed an authority, altered testimony, replaced a product identifier, added unsupported material evidence, injected a causation override, and tampered with an intermediate stage after downstream generation. Each control either changed the chain or was rejected by the evaluator.

## Non-claims

This package does not establish real legal correctness, filing readiness, real product identification, real exposure, dose, causation, liability, independent fresh-generation provenance, external verification, or production deployment.

## Reproduction

```bash
python3 -B run_chain.py input.json run_1
python3 -B run_chain.py input.json run_2
python3 -B independent_evaluator.py
python3 -B chain_controls.py
```
