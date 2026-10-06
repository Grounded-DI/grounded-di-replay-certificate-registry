# New York City Exact-Output Determinism Evidence

## Purpose

This is a curated evidence index inside the Grounded DI Replay Certificate Registry. It presents a compact public record of exact-input → exact-output replay at the controlled execution boundary.

The evidence is organized around one common replay/control architecture expressed through multiple outputs and domains. The five NYC categories below are reviewer questions, not five independent methods or five required new demonstrations.

The relevant system-level property is:

> Under declared input, policy, code, configuration, environment, serialization, and authorization conditions, a controlled execution can produce reproducible decision records and/or output artifacts, while a declared material change can produce a controlled change or refusal.

Model-level stochastic generation and system-level controlled/replayable execution are separate layers. Where a model participates, the evidence here concerns the governed decision or output artifact at the system boundary.

## Common method

```text
declared input, policy, configuration, and state
  → canonical record
  → explicit evaluation
  → decision or refusal
  → controlled output boundary
  → receipt, hash, or audit trace
  → replay or verification
```

The implementations use different domain rules and, in some cases, different canonical serialization formats. The recurring method elements are binding, explicit evaluation, controlled state/output, preserved evidence, and replay or verification.

See [METHOD.md](METHOD.md) for the shared invariants and implementation differences.

## Five-minute reviewer path

1. Read [METHOD.md](METHOD.md) for the common control/replay pattern.
2. Open [VerdictBridge Demo 3](../2026-10-05-verdictbridge-punitive-control-v1/README.md), the strongest end-to-end exact-replay witness.
3. Open [Expiry and Policy Replay](../2026-09-10-di2-expiry-policy-v1/README.md) for refusal and export-boundary evidence.
4. Open [ChainGate](../../10_ChainGate_Demo_Record.txt) for a material configuration change that changes the result.
5. Open [FlightGate](../../08_FlightGate_Demo_Record.txt) for the same replay/control pattern in a non-legal domain.
6. Open [Global Multirow Coercivity](../../02_Global_Multirow_Coercivity_Master_Certificate_Intake_Record_v2.txt) for a packaging and revalidation boundary.
7. Use [EVIDENCE-MAP.md](EVIDENCE-MAP.md) for the evidence matrix, classification, and commit references.

## Primary evidence set

| NYC reviewer question | Primary evidence | What to inspect |
|---|---|---|
| 01 — Exact input / exact output | [VerdictBridge Demo 3](../2026-10-05-verdictbridge-punitive-control-v1/README.md) | Three fresh processes, five artifact comparisons, hashes, separate verifier |
| 02 — Material change / controlled change | [ChainGate](../../10_ChainGate_Demo_Record.txt) | 8.0 → 7.9 configuration change: RELEASE → HOLD |
| 03 — Invalid or disallowed input / refusal | [Expiry and Policy Replay](../2026-09-10-di2-expiry-policy-v1/README.md) | Expiry, policy, malformed-input, and destination controls before export |
| 04 — Cross-domain replay | [FlightGate](../../08_FlightGate_Demo_Record.txt) | FLY/NO_FLY configuration-driven replay outside legal work |
| 05 — Scope / revalidation boundary | [Global Multirow Coercivity](../../02_Global_Multirow_Coercivity_Master_Certificate_Intake_Record_v2.txt) | Preserved rejection, packaging repair, clean-room replay, and fixed mathematical scope |

These five records are linked evidence instances. They are not five separate implementations of the method.

## Verification

The strongest local reproduction path is VerdictBridge Demo 3. Extract its public ZIP and run from the extracted package root:

```bash
python3 -B source/verify_release.py
python3 -B source/verify.py
python3 -B source/acceptance.py
shasum -a 256 -c SHA256SUMS.txt
```

The expiry/policy source has a second runnable path:

```bash
python3 -B verify.py
python3 -B acceptance.py
shasum -a 256 -c SHA256SUMS.txt
```

On Linux, `sha256sum -c` may be used in place of `shasum -a 256 -c`. The linked records provide their own package, manifest, and verification instructions where applicable.

## Provenance

The selected evidence was audited against registry commit `90b0b0cbe5eb244412b2c6befab273a137c51c3a`.

The selected evidence preserves these relevant references:

- VerdictBridge Demo 3 public release: `90b0b0cbe5eb244412b2c6befab273a137c51c3a`.
- VerdictBridge original reference evidence: `8472b48470b6c35a3ad2778f0819f36d4ddaef1b`.
- Expiry and Policy Replay: `3286b58800c4d97519b707fa8df5b4348d9a61a8`.
- ChainGate and FlightGate root records: current-tree pin `90b0b0cbe5eb244412b2c6befab273a137c51c3a`; historical root-record commit `33ce180aacee6503f6f3994fc643cb9f77507752`.
- Global Multirow attestation materials: `4cfc13219edb4f694705827a02bed0b25932662c`.

## Further registry evidence

The broader registry contains additional evidence instances, including Replayable Authorization, Single-Use and Crash Recovery, BriefWise, FastPath, StormWise, CleanWaterWise, exact mathematics, the earlier VerdictBridge replay, Replayable Damages, and JoyWise. This index links the smallest set needed to make the common method legible in approximately five minutes.

## Publication approach

This directory is an index, not a benchmark treadmill. The initial five links can be published together because they fill distinct reviewer questions. Future additions should contribute a new domain, failure mode, engine/version boundary, longitudinal result, or materially stronger validation.
