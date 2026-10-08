# Grounded DI Replay Certificate Registry

A public technical-evidence registry for replayable decisions, rule-gated authorization, artifact identity, and audit-ready execution records.

**Published by Grounded DI LLC · Creator / Operator: Mark S. Weinstein · Public repository established July 23, 2026**

## Overview

This repository preserves runnable demonstrations, certificate intake records, verification artifacts, and cryptographic manifests from Grounded DI work across legal analysis, exact mathematics, environmental routing, aviation, weather, logistics, and controlled file export.

The central design goal is to make an execution inspectable: bind the inputs and governing policy, evaluate explicit rules, record the resulting state, preserve the output and audit history, and verify the record through replay or source-based recalculation. In this repository, *deterministic* refers to rule-governed or reproducible behavior under the stated inputs, code, environment, and serialization conditions. It is not a claim that every underlying proposition is universally correct.

The registry includes four runnable Python demonstrations and ten numbered evidence records. It also preserves later replay records for BriefWise DI² and a sealed FastPath rule-execution workload.

> **Repository scope:** The public evidence supports the result stated by each record—such as byte identity, fresh local replay, boundary enforcement, or exact arithmetic. Broader conclusions are not inferred from hashes alone. Certificates in the runnable demonstrations are local, unsigned project records.

## VerdictBridge Demo 3 — Selective Outcome Replay

[Demonstration and runnable evidence](demos/2026-10-05-verdictbridge-punitive-control-v1/README.md) · [PDF](demos/2026-10-05-verdictbridge-punitive-control-v1/package/VerdictBridge_Demo3_Report.pdf) · [Complete ZIP](demos/2026-10-05-verdictbridge-punitive-control-v1/VerdictBridge_Demo3_Public_v1.zip)

A newly implemented local evaluator produced the declared selective result across three fresh executions with five matching artifact hashes and direct byte comparisons, and refused the inadmissible-hearsay control before export. Preserved original reference evidence, a separate internal verifier, and measured execution records are included. This is a finite closed-world demonstration; original-engine execution, native VerdictBridge reproduction, universal model determinism, and external certification are not claimed.

## VerdictBridge Demo 3 - Fresh Replay (October 7, 2026)

[Demonstration](demos/2026-10-07-verdictbridge-demo3-fresh-replay/README.md) · [PDF](demos/2026-10-07-verdictbridge-demo3-fresh-replay/package/Fresh_Replay_Report.pdf) · [Complete ZIP](demos/2026-10-07-verdictbridge-demo3-fresh-replay/VerdictBridge_Demo3_Fresh_Replay_Public_v1.zip)

Three fresh executions reproduced the five canonical artifacts byte for byte against the earlier Demo 3 evidence and refused the inadmissible-hearsay export. Internal verification; unaffiliated review pending. This is a replay of the existing finite benchmark, not a new demonstration of universal model determinism. Fresh receipts record real process IDs/timestamps outside the canonical byte boundary.

## NYC Exact-Output Determinism Evidence

The [NYC Exact-Output Determinism Evidence](demos/nyc-exact-output-determinism/README.md) directory is a curated index of existing registry evidence relevant to exact-input → exact-output replay. It explains the common controlled-execution method and links to selected legal, authorization, logistics, aviation, and mathematical records without duplicating their binaries.

## Why It Matters

Outputs alone do not show which inputs were authorized, which policy controlled execution, why a state changed, whether a release boundary was enforced, or whether the evidence can be replayed. This registry makes those questions reviewable through structured records, explicit state transitions, negative controls, manifests, checksums, and executable verification where supplied.

## Evaluation Value

Technical and commercial reviewers can use this repository to evaluate Grounded DI's approach to:

- binding an action to exact content, destination, policy, scope, and validity conditions;
- blocking execution when a required condition changes or evidence is malformed;
- replaying a recorded decision in a fresh process;
- separating artifact identity from fresh-generation provenance;
- preserving uncertainty after an interrupted write rather than silently resetting state; and
- packaging inputs, decisions, outputs, history, and integrity data for audit.

These public demonstrations provide a concrete starting point for a scoped proof of concept without requiring disclosure of private runtime materials.

## Key Results

| Record | Implemented result | Evidence available |
| --- | --- | --- |
| [Replayable Authorization](demos/2026-09-10-di2-authorization/README.md) | Exact authorization permits a synthetic export; a changed destination is denied before a file-open attempt. Fresh-process replay reproduces the canonical decision record. | Runnable Python package, three negative controls, ZIP checksum, replay identity, unsigned local certificate |
| [Expiry and Policy Replay](demos/2026-09-10-di2-expiry-policy-v1/README.md) | Enforces `issued_at <= execution_time < expires_at`, binds the complete policy object, and rejects same-version policy changes, malformed evidence, and altered artifacts. | Browsable source, 25 recorded cases, 10 boundary checks, six negative controls, reference evaluator, ZIP and manifests |
| [Single-Use and Crash Recovery](demos/2026-09-10-di2-single-use-crash-v1/README.md) | Implements `UNUSED -> RESERVED -> COMPLETED` or `RESERVED -> UNCERTAIN`; 20 competing processes produce one completed export and 19 completed-state acknowledgments. | Browsable source, 14 scenarios, three process-kill cases, six negative controls, separate history checker, ZIP and manifests |
| [BriefWise Fresh Local Replay](BriefWise_DI2_GitHub_Post.md) | Preserves a public replay package and checksum for a legal-workflow record. | Post, public ZIP, SHA-256 checksum, and visual replay evidence |
| FastPath rule-execution replay | Two fresh executions produced byte-identical explicit decision records and run archives; a source-based verifier rejected a deliberately altered derivation. | Public result description and [`FastPath_5_6_Instant_Day_One_Canonical_Replay_Certificate.pdf`](FastPath_5_6_Instant_Day_One_Canonical_Replay_Certificate.pdf) |

## Technical Highlights

### Authorization-bound execution

The runnable harnesses bind the proposed action to declared evidence before export. Depending on the demonstration, the bound record includes the report hash, action, destination, full policy hash, scope, state, authorization identifier, and validity interval. A mismatch routes to denial or refusal rather than an attempted write.

### Canonical records and replay identity

The authorization series uses `DI2-ASCII-JSON-LF-1`, a documented restricted JSON serialization format with sorted object keys, compact separators, ASCII escaping, and one final line feed. It is expressly not presented as full JSON Canonicalization Scheme compliance. SHA-256 binds the canonical replay record and identified evidence.

### Independent logic paths within the project

The expiry demo includes a separately implemented reference evaluator. The crash-recovery demo includes a separate transition-history checker. They do not import the primary decision logic, although they share specified serialization utilities or were authored against the same project specification. Their agreement is a useful internal cross-check, not external independent verification.

### Conservative crash state

The single-use demo durably reserves an authorization before export. If interruption occurs after reservation but before verified completion, the state becomes `UNCERTAIN` and does not return to `UNUSED`. The documented property is at most one export-creation attempt per authorization within the cooperative local store, with possible noncompletion or uncertainty—not exactly-once delivery or system-wide enforcement.

### Evidence-aware claims

The numbered intake records distinguish computation from packaging, identical bytes from independent generation, local replay from external review, and corrected releases from erased history. This separation is a core feature of the registry rather than a limitation added after the fact.

## Architecture

```text
Authorized input and policy
  -> canonical evidence record
  -> rule and validation gates
  -> decision or execution state
  -> controlled output boundary
  -> audit history and receipt
  -> replay, recalculation, and hash verification
```

## How It Works

1. **Bind the evidence.** Exact inputs, policy, scope, destination, and relevant code or configuration are recorded.
2. **Evaluate declared rules.** The harness computes a result from explicit conditions and rejects missing, altered, expired, or malformed evidence.
3. **Route the state.** The record captures an allowed, denied, held, reserved, completed, or uncertain outcome as applicable.
4. **Control the boundary.** File output occurs only after the required authorization checks succeed.
5. **Preserve the history.** Results, state transitions, hashes, receipts, and manifests create an inspectable record.
6. **Verify again.** Fresh-process replay, a separate project checker, exact arithmetic, checksum validation, or byte comparison tests the stated invariant.

## Numbered Demo Registry

| No. | Demonstration | Repository-supported result | Recorded status |
| ---: | --- | --- | --- |
| 01 | VerdictBridge Five-Hash Replay | Five corresponding artifact-hash fields match across two legal-analysis runs; the packaged artifacts are byte-identical. | Full pass / `VERDICT_READY` |
| 02 | Global Multirow Coercivity | Preserves the initial reproducibility rejection and a documented packaging-only repair while retaining the immutable mathematical artifacts. | Full pass after documented repair |
| 03 | Replayable Damages Mini Demo | Reproduces fixed damages arithmetic and byte-identical archives under the stated synthetic inputs. | Full pass; demonstration, not case-value prediction |
| 04 | JoyWise Afterglow | Establishes exact UTF-8 text identity, including line endings and final-newline state. | Full pass |
| 05 | Erdős 124 Fixed Certificate | Fresh local verification for the fixed scope `D = {3,4,7}, k = 1`, covering 3,119,493 residue-admissible systems. | Full pass / fresh local replay; external review not recorded |
| 06 | Erdős 390 Thirteen-Layer Lower Bound | Checks an exact rational partial lower-bound certificate with 13 layers, 104 dual inequalities, nine tight constraints, and exact primal-dual equality. | Full pass / fresh local replay; expert-review candidate |
| 07 | CleanWaterWise | Routes seven synthetic water-quality records to `PASS`, `REVIEW`, or `HALT` under disclosed rules. | Pass; fresh-generation provenance unverified |
| 08 | FlightGate | Applies disclosed `FLY` / `NO_FLY` rules to ten synthetic records, including exact boundaries and fail-closed missing fields. | Pass; fresh-generation provenance unverified |
| 09 | StormWise | Recomputes a synthetic weighted tornado-index formula and threshold classifications using exact rational arithmetic. | Pass; fresh-generation provenance unverified |
| 10 | ChainGate | Applies seven disclosed rules to ten synthetic shipment records with exact decimal boundaries and multi-trigger reporting. | Pass; fresh-generation provenance unverified |

The detailed scope, identifiers, artifact hashes, and non-claims for each demonstration remain in the corresponding numbered intake record at the repository root.

## Repository Structure

```text
.
├── 01_... through 10_...                 # master-certificate intake records
├── demos/
│   ├── 2026-09-10-di2-authorization/     # packaged runnable harness
│   ├── 2026-09-10-di2-expiry-policy-v1/  # browsable source and evidence
│   └── 2026-09-10-di2-single-use-crash-v1/
├── Verdictbridge_demo*/                  # corresponding run artifacts
├── Global_Multirow_Coercivity_.../       # acceptance and integrity records
├── BriefWise_DI2_...                     # replay post, ZIP, checksum, and PDF
├── *Gate_Demo*.zip                       # packaged synthetic routing records
├── FastPath_5_6_...pdf                   # replay certificate
├── FixedCase_D347_...pdf                 # fixed-case mathematics record
└── README.md
```

## Quick Start

Clone the repository:

```bash
git clone https://github.com/Grounded-DI/grounded-di-replay-certificate-registry.git
cd grounded-di-replay-certificate-registry
```

The browsable demonstrations require Python 3.9+ on macOS or a POSIX platform. They use only the Python standard library and make no network or model calls during verification.

Run the expiry and policy demonstration:

```bash
cd demos/2026-09-10-di2-expiry-policy-v1/source
python3 -B verify.py
python3 -B acceptance.py
sha256sum -c SHA256SUMS.txt
```

Run the single-use and crash-recovery demonstration:

```bash
cd demos/2026-09-10-di2-single-use-crash-v1/source
python3 -B verify.py
python3 -B acceptance.py
sha256sum -c SHA256SUMS.txt
```

The first authorization demo is distributed inside its ZIP:

```bash
cd demos/2026-09-10-di2-authorization
sha256sum -c DI2_Replayable_Authorization_Demo_20260910_1110.zip.sha256.txt
unzip DI2_Replayable_Authorization_Demo_20260910_1110.zip
cd DI2_Replayable_Authorization_Demo_20260910_1110
python3 -B verify.py
python3 -B acceptance.py
sha256sum -c SHA256SUMS.txt
```

On macOS, replace `sha256sum -c` with `shasum -a 256 -c`.

## Validation and Testing

| Evidence | Repository record | Executed during September 16, 2026 review |
| --- | --- | --- |
| Replayable Authorization | Fresh-process and fresh-file execution; destination mismatch denied before write; three altered-copy controls | `verify.py` and `acceptance.py` passed; replay SHA-256 `9192da71d870ddcdcb9dfddfc2b695a00365acf87910cee9b4047590d5ac4632` |
| Expiry and Policy Replay | 25 recorded cases, 10 boundary checks, six altered-copy controls, reference comparison, bounded real-clock test | `verify.py` and `acceptance.py` passed; replay SHA-256 `08f6750447a0f923d1b175a436f9ef03f98d0b50b755b52e276aed05bb410fe8` |
| Single-Use and Crash Recovery | 14 scenarios, 20-process contention, three process-kill cases, six altered-copy controls | `verify.py` and `acceptance.py` passed; replay SHA-256 `c02ff6c5802c398b4a20a75c48a05ad11a32c766fd507bc2f16e16befb3351c8` |
| Python source | Three runnable packages | All Python files compiled successfully with `compileall` |
| Published packages | 16 ZIP files across the registry | Every ZIP passed archive-integrity testing |
| Published checksum manifests | Four package checksum files, two source manifests, and two mathematical attestation manifests | Every listed file passed SHA-256 verification |

The concurrency acceptance run reproduced the required safety outcome, but its process identifiers, winning process, event order, and resulting identity may differ between runs. Replay identity applies to the same recorded history; it does not imply deterministic operating-system scheduling.

## Example Use Cases

### Demonstrated here

- Exact action authorization tied to content, destination, policy, and scope.
- Expiry and policy-change handling at a file-export boundary.
- Single-use authorization with durable reservation and conservative crash recovery.
- Replayable legal-workflow and exact-mathematics evidence packages.
- Synthetic threshold routing for water, aviation, weather, and logistics records.
- Artifact-integrity checking through canonical records, manifests, and SHA-256.

### Potential integration scenarios

Subject to the applicable implementation and commercial terms, the demonstrated patterns could support controlled write-back, approval-bound export, audit-receipt generation, policy-gated workflow actions, one-time execution tokens, or replayable decision support. These are integration scenarios, not claims of current customer deployment.

## Commercial and Integration Context

A focused evaluation can begin with one high-value action boundary:

1. identify the proposed action and downstream system;
2. define the evidence, policy, authorization, and expiration conditions;
3. specify fail-closed states and human escalation points;
4. agree on receipts, replay data, and acceptance tests; and
5. run a synthetic or appropriately governed proof of concept before production integration.

Commercial licensing and integration inquiries: [mark@groundeddi.ai](mailto:mark@groundeddi.ai).

## Authorship and Provenance

This repository contains versioned development records and provenance artifacts designed to preserve technical history and authorship traceability.

- Git history identifies **Grounded DI LLC** as the repository publisher beginning July 23, 2026.
- Repository records identify **Mark S. Weinstein** as creator and operator.
- Numbered intake records preserve scope, status, identifiers, hashes, and the chronology of corrections.
- Runnable demonstrations bind code, evidence, decision records, and outputs through manifests and replay identities.
- The mathematical acceptance record preserves the prior rejection rather than rewriting the historical state.

Commits, timestamps, manifests, and hashes are useful provenance and integrity evidence. They do not independently establish legal ownership, inventorship, patent priority, or substantive correctness.

## Intellectual Property

Copyright © 2026 Grounded DI LLC. Project and product names are used for identification and attribution.

No open-source license is granted by this repository. Publicly accessible materials remain subject to applicable copyright, trademark, contractual, and other rights except where expressly stated otherwise. Nonpublic implementation materials are outside the scope of this repository.

Certain subject matter is associated in repository records with pending U.S. utility non-provisional patent applications. The filing index below is a public project record supplied by Grounded DI LLC and is preserved for chronology; it is not an assertion of issuance, allowance, priority entitlement, or claim scope.

<details>
<summary><strong>Public filing index — status recorded July 25, 2026</strong></summary>

| No. | Domain / Nickname | Application No. | Received | Title |
|---:|---|---|---|---|
| 1 | Law / BriefWise | 19/686,791 | 24 May 2026 | Deterministic Intelligence Systems and Methods for Controlled Pre-Output Assembly of Legal Outputs Using Authority Binding and Filing-Integrity Validation |
| 2 | Structured Output | 19/694,947 | 1 Jun 2026 | Rule-Based Logic Control, Structured Output Governance, and Controlled Presentation of Generative AI Outputs |
| 3 | Med / Radiology | 19/704,303 | 10 Jun 2026 | Radiological Image Interpretation, Diagnostic Support, Clinical Review Routing, Audit Verification, and Runtime Authorization |
| 4 | DI Cross-Domain | 19/705,787 | 11 Jun 2026 | Cross-Domain Controlled Output Assembly and Release |
| 5 | Engineering / Rockets | 19/706,930 | 12 Jun 2026 | Controlled State Assembly, Subsystem Propagation Analysis, Audit Verification, Replay Validation, and Runtime Authorization |
| 6 | Environment / Water | 19/710,164 | 16 Jun 2026 | Clean-Water Risk Assessment and Public-Health Advisory Release Control |
| 7 | Finance | 19/713,347 | 18 Jun 2026 | Financial Transaction Authorization and Output Release Control Using Metric Replay, Verification, State Precedence, and Interface Authorization |
| 8 | DIA | 19/715,156 | 22 Jun 2026 | Rule-Governed, Domain-Scoped, Audit-Traceable Control of Generative Output States |
| 9 | Grounded DI Engine | 19/716,065 | 22 Jun 2026 | Pre-Commitment Logic-State Authorization, Model-Interface Governance, Audit-Traceable Validation, and Controlled Delivery |
| 10 | Weather Station | 19/717,640 | 23 Jun 2026 | Rule-Governed, Corridor-Scoped, Audit-Traceable Control of Weather-Alert Release |
| 11 | PIDBot | 19/720,483 | 25 Jun 2026 | Product-Identification Analysis, Exposure-Role Classification, Audit-Traceable Replay Verification, and Controlled Delivery of Litigation Artifacts |
| 12 | VerdictBridge | 19/720,877 | 25 Jun 2026 | Controlled Litigation Artifact Generation, Validation, Replay Verification, and Authorized Output Delivery |
| 13 | DI² | 19/722,923 | 28 Jun 2026 | Divergence Containment and Convergence Restoration in Deterministic Execution Architectures |
| 14 | AGDI | 19/722,955 | 28 Jun 2026 | State-Bound Continuation Control of Generative Agent Operations |
| 15 | DEC | 19/724,532 | 29 Jun 2026 | Deterministic Execution Control Using Constraint-Tree Enforcement, Agent-Type Classification, Escalation Routing, Audit-Linked Rollback, and Controlled Output Authorization |
| 16 | AGIA | 19/724,908 | 30 Jun 2026 | Pre-Observability Expression-State Authorization and Output-Propagation Control of Machine-Generated Outputs |
| 17 | ELOC | 19/726,030 | 30 Jun 2026 | Entropy-Linked Override Chain Enforcement in Generative Artificial Intelligence Systems |
| 18 | Runtime (DIP / Scroll Architecture) | 19/726,765 | 30 Jun 2026 | DI Runtime Authorization, Canonical Receipt Binding, and Replay-Verified Execution Control |
| 19 | DI-AGI | 19/726,890 | 30 Jun 2026 | Runtime-Governed Artificial-Intelligence Execution, Replay Verification, and Release Authorization |
| 20 | DepoBot | 19/730,739 | 2 Jul 2026 | Deterministic Intelligence Systems and Methods for Controlled Deposition Artifact Generation, Validation, Replay Verification, and Authorized Output Delivery |
| 21 | DI Hazard Intelligence | 19/736,923 | 9 Jul 2026 | Deterministic Intelligence Systems and Methods for Threshold-Gated Multi-Hazard Evaluation and Audit-Traceable Emergency Assistance |
| 22 | DI LLM Entropy Control | 19/748,124 | 20 Jul 2026 | Systems and Methods for Deterministic Entropy Governance and Entropy-Linked Override Enforcement in Generative Artificial Intelligence Systems |
| 23 | Shopping / Consumer | 19/765,102 | 24 Jul 2026 | Deterministic Intelligence Systems and Methods for Consumer Decision-Control, Evidence-Linked Commercial Assessment, Transaction-State Authorization, and Replay |

</details>

## Citation and Attribution

Recommended citation:

> Grounded DI LLC. (2026). *Grounded DI Replay Certificate Registry* [Software and public technical-evidence registry]. GitHub. https://github.com/Grounded-DI/grounded-di-replay-certificate-registry

When referencing a specific demonstration, cite its numbered intake record or dated demo directory and preserve the stated scope and status.

## Status

**Active public replay, verification, and provenance registry.** The repository supports runnable technical evaluation, artifact-integrity review, chronology preservation, and preliminary commercial diligence. The authorization series is a local demonstration harness; production integrations and private runtime materials are maintained separately where applicable.

## Contact and Collaboration

For technical evaluation, controlled demonstrations, integration discussions, or commercial licensing, contact [Grounded DI LLC](mailto:mark@groundeddi.ai). Identify the action boundary or evidence workflow you want to evaluate and the acceptance criteria that matter to your organization.

---

#DeterministicAI #AIValidation #Auditability #Replayability #AIInfrastructure #AIGovernance #Provenance #GroundedDI
