# Evidence index

Use this page to find a problem, see what the example does, and determine what you can inspect. All descriptions are summaries of the linked records, not new executions. Most examples use fictional inputs and run locally; the individual record defines its scope.

**Runnable** identifies public source or a public package indicated by the record. **Evidence** describes what is available in this repository; “public” does not mean every underlying record is published. “Not in this record” means the linked historical summary does not itself provide the runnable package. Follow the record for exact dependencies, test results, and limitations.

Many examples use multiple output files or “boundaries.” In several seven-boundary examples, the seventh file commits to the first six; it is not a seventh independent verification. A file hash identifies bytes against a reference, while a direct comparison checks the bytes themselves. Neither alone proves that the underlying facts are true.

## Start by evidence type

- **Controlled action and recovery:** [Authorization](demos/2026-09-10-di2-authorization/README.md), [expiry and policy](demos/2026-09-10-di2-expiry-policy-v1/README.md), and [single use and crash recovery](demos/2026-09-10-di2-single-use-crash-v1/README.md). Use the [evaluator walkthrough](EVALUATOR_GUIDE.md) to run the expiry example.
- **Synthetic domain workflows:** Browse the legal, finance, insurance, water, supply, and logistics sections below.
- **Mathematical and source-based calculations:** See the water, science, and exact mathematics section below. Check each record for its claim and source boundary.
- **Historical summaries:** Some entries publish a report and identifiers while retaining the underlying run archives elsewhere; their availability is stated in the relevant row.

The [evidence matrix](EVIDENCE_MATRIX.md) provides a file-level availability map for every demo and benchmark directory.

## Replay families

- **VerdictBridge Demo 3:** [October 5 selective-outcome demonstration](demos/2026-10-05-verdictbridge-punitive-control-v1/README.md), [October 7 fresh replay](demos/2026-10-07-verdictbridge-demo3-fresh-replay/README.md), [October 8 published-release replay](demos/2026-10-08-verdictbridge-demo3-published-replay/README.md), and [October 16 replay lanes](benchmarks/verdictbridge-demo3-replays-2026-10-16/README.md). These are successive records of a shared benchmark, not four separate domain demonstrations.
- **Seven-hash series:** [October 19 closure](benchmarks/2026-10-19-seven-hash-replay-closure/README.md), [November 1 fresh replay](benchmarks/2026-11-01-seven-hash-fresh-replay/README.md), [November 1 independent local replay](benchmarks/2026-11-01-seven-hash-independent-local-replay/README.md), and [November 1 evening replay](benchmarks/2026-11-01-seven-hash-replay-2124-et/README.md). The records distinguish fresh computation of six boundaries from reconstruction of the existing historical ZIP as the seventh; the referenced raw archives are not hosted in these summaries.

## Controlled actions, release, and recovery

| Record | What it demonstrates or records | Runnable material | Evidence availability |
| --- | --- | --- | --- |
| [Di2 authorization](demos/2026-09-10-di2-authorization/README.md) | Synthetic export authorized for a specified destination; a changed destination is refused. | ZIP | Public package and certificate |
| [Di2 expiry policy v1](demos/2026-09-10-di2-expiry-policy-v1/README.md) | Checks expiration and full-policy changes before a local export. | Source + ZIP | Public source, results and certificate |
| [Di2 single use crash v1](demos/2026-09-10-di2-single-use-crash-v1/README.md) | Tests single-use authorization with competing local processes and crash recovery. | Source + ZIP | Public source and recorded outcomes |
| [Expiry policy fresh](demos/2026-10-27-expiry-policy-fresh-replay/README.md) | Records two fresh replays of the earlier expiry demo. | Earlier source linked | Public historical observations; earlier source public |
| [Payment retry](demos/2026-11-01-payment-retry-replay/README.md) | Holds a consumed request after an uncertain response; a separately approved new ID can cause a second synthetic effect. | Source | Public synthetic results; original gate exercise private |
| [Releasegate promotion](benchmarks/2026-11-01-releasegate-promotion-replay/README.md) | Checks a fictional candidate against test, policy, approval and destination evidence before a local write. | Source + ZIP | Public runs and controls |
| [Lighthouse releasegate](benchmarks/2026-11-01-lighthouse-releasegate-replay/README.md) | Evaluates a fictional release and tests altered approval, policy and decision records. | ZIP | Public package and verification record |
| [Releasegate v2 local write](benchmarks/2026-11-01-releasegate-v2-local-write/README.md) | Adds an authorized local write and tests changed paths and other refusals. | ZIP | Public package and extraction recheck |
| [Releasegate v3 lost confirmation](benchmarks/2026-11-01-releasegate-v3-lost-confirmation/README.md) | Exercises retry after a local write completes without confirmation. | ZIP | Public package and extraction recheck |
| [Releasegate v4 authenticated receipt](benchmarks/2026-11-01-releasegate-v4-authenticated-receipt/README.md) | Uses a local authenticated receipt to check a retry after lost confirmation. | ZIP | Public package and extraction recheck |
| [Releasegate locals](benchmarks/2026-11-03-releasegate-local-replays/README.md) | Documents additional historical ReleaseGate replays of a frozen package. | Earlier source linked | Summary public; run archives privately retained |
| [Microsoft DI² v0.3.1 fresh rerun: attribution correction](benchmarks/2026-10-21-microsoft-di2-v031-fresh-rerun/Source_Attribution_Correction.md) | Corrected target is Microsoft Agent Governance Toolkit at the pinned commit; the earlier report named a different repository. The correction did not locate the later execution receipts. [Historical report](benchmarks/2026-10-21-microsoft-di2-v031-fresh-rerun/Grounded_DI_Microsoft_DI2_v031_Fresh_Rerun_Report.md). | Executable target snapshots and payloads omitted | Public correction, report and exhibit; later execution receipts not located in attribution review |

## Legal workflows and evidence

| Record | What it demonstrates or records | Runnable material | Evidence availability |
| --- | --- | --- | --- |
| [Verdictbridge punitive control v1](demos/2026-10-05-verdictbridge-punitive-control-v1/README.md) | Replays a fictional selective summary-judgment outcome and refuses a hearsay-based candidate. | Source + ZIP | Public package and reference evidence; prompt omitted |
| [Verdictbridge demo3 fresh](demos/2026-10-07-verdictbridge-demo3-fresh-replay/README.md) | Replays the existing Demo 3 with fresh local processes and tamper controls. | ZIP | Public derivative; some local controller and paths omitted |
| [Verdictbridge demo3 published](demos/2026-10-08-verdictbridge-demo3-published-replay/README.md) | Replays a pinned published Demo 3 release with hearsay and tamper controls. | ZIP | Public derivative; some local material omitted |
| [Verdictbridge demo3s 2026 10 16](benchmarks/verdictbridge-demo3-replays-2026-10-16/README.md) | Records two isolated replays of existing VerdictBridge Demo 3 packages. | Packages within linked lanes | Public replay archives and shortfall record |
| [Legal evidences](benchmarks/2026-10-19-legal-evidence-replays/README.md) | Runs three synthetic lanes for authority, testimony contradictions and product/exposure evidence. | Source | Public lane outputs and checks |
| [Integrated legal chain](benchmarks/2026-10-19-integrated-legal-chain-replay/README.md) | Connects authority, testimony, product identification and verdict stages in a fictional matter. | Source | Public inputs, stage outputs and controls |
| [Expertscope opinion basis](benchmarks/2026-10-19-expertscope-opinion-basis-replay/README.md) | Traces fictional expert statements to source fragments and evaluates altered records. | Source | Public report, expected outputs and controls |
| [Seven boundary legal deadline](benchmarks/2026-11-01-seven-boundary-legal-deadline/README.md) | Calculates a fictional calendar deadline and holds incomplete cases. | Source | Public inputs, runs and tests |

## Finance, invoices, and insurance

| Record | What it demonstrates or records | Runnable material | Evidence availability |
| --- | --- | --- | --- |
| [Seven boundary invoice reconciliation](benchmarks/2026-10-27-seven-boundary-invoice-reconciliation/README.md) | Applies duplicate and purchase-order-limit rules to a fictional invoice batch. | Source | Public inputs, comparisons and tests |
| [Financewise transaction covenant](benchmarks/2026-10-19-financewise-transaction-covenant-replay/README.md) | Connects synthetic transaction evidence to arithmetic and a covenant disposition. | Source + ZIP | Public staged outputs and controls |
| [Synthetic insurance claims](demos/2026-11-04-synthetic-insurance-claims/README.md) | Routes fictional damage claims using an invented policy. | Source | Public specification, outputs and test results |

## Water, science, and exact mathematics

| Record | What it demonstrates or records | Runnable material | Evidence availability |
| --- | --- | --- | --- |
| [Arsenic water](demos/2026-11-04-arsenic-water-replay/README.md) | Compares fictional arsenic values under a declared numerical rule; retains a report correction. | Source | Public outputs, audit and correction |
| [Nitrate screening](demos/2026-11-04-nitrate-screening-replay/README.md) | Compares fictional values to a nitrate threshold and binds exact input bytes. | Source | Public v2 outputs and tests; v1 audit evidence private |
| [Chemistry physics calorimetry](benchmarks/2026-11-01-chemistry-physics-calorimetry-replay/README.md) | Recomputes a fictional energy-transfer and temperature-change calculation. | Source + ZIP | Public runs and checks |
| [Nist water source bound](benchmarks/2026-11-01-nist-water-source-bound-replay/README.md) | Uses a transcribed NIST water property in a source-bound calculation. | Source + ZIP | Public transcription, outputs and checks |
| [Nist water shomate temperature](benchmarks/2026-11-01-nist-water-shomate-temperature-replay/README.md) | Integrates a transcribed heat-capacity equation over a synthetic temperature interval. | Source + ZIP | Public transcription, outputs and checks |
| [Seven hash closure](benchmarks/2026-10-19-seven-hash-replay-closure/README.md) | Records six fresh computation boundaries and reconstruction of an existing historical ZIP. | Not in this record | Summary and hashes public; referenced archives not hosted |
| [Seven hash fresh](benchmarks/2026-11-01-seven-hash-fresh-replay/README.md) | Records later fresh computation and historical-payload repackaging. | Not in this record | Summary public; new raw archive retained elsewhere |
| [Seven hash independent local](benchmarks/2026-11-01-seven-hash-independent-local-replay/README.md) | Records additional project-local computation, checking and repackaging. | Not in this record | Summary public; raw archive private |
| [Seven hash 2124 et](benchmarks/2026-11-01-seven-hash-replay-2124-et/README.md) | Records another computation and repackaging run. | Not in this record | Summary public; supplemental archive private; some ZIP copies not retained |

## Supply, logistics, and resource allocation

| Record | What it demonstrates or records | Runnable material | Evidence availability |
| --- | --- | --- | --- |
| [Seven boundary cold chain](benchmarks/2026-10-27-seven-boundary-cold-chain-replay/README.md) | Applies fictional temperature limits to a shipment. | Source | Public inputs, runs and tests |
| [Seven boundary water](benchmarks/2026-10-27-seven-boundary-water-replay/README.md) | Allocates a fictional water supply under a fixed priority rule. | Source | Public runs and correction history |
| [Shelterwise priority drift](benchmarks/2026-10-19-shelterwise-priority-drift-replay/README.md) | Tests fictional shelter priorities, capacity and uncertain allocations. | Source + ZIP | Public stage outputs and controls |
| [Delivery cold storage](benchmarks/2026-11-02-delivery-cold-storage-replay/README.md) | Reconciles fictional shipment, temperature and quantity records. | ZIP | Public package and extraction audit |
| [Delivery inventory reconciliation](benchmarks/2026-11-02-delivery-inventory-reconciliation-replay/README.md) | Compares fictional order, shipment and receiver records. | ZIP | Public package and extraction audit |
| [Flood delivery alternate route](benchmarks/2026-11-02-flood-delivery-alternate-route-replay/README.md) | Allocates fictional supplies over a network with a closed road. | ZIP within evidence ZIP | Public evidence package and audit |
| [Flood depot delivery](benchmarks/2026-11-02-flood-depot-delivery-replay/README.md) | Routes fictional depot supplies under road-closure rules. | ZIP | Public package and extraction audit |
| [Inventory recall frozen correction](benchmarks/2026-11-02-inventory-recall-frozen-correction/README.md) | Holds a fictional recalled lot while preserving the earlier receipt and correction history. | Not in this record | Summary public; evidence package private |

## Cross-domain collections

| Record | What it demonstrates or records | Runnable material | Evidence availability |
| --- | --- | --- | --- |
| [Three lane 2026 10 17](benchmarks/three-lane-replay-2026-10-17/README.md) | Collects isolated CleanWaterWise, expiry and FlightGate replay lanes. | See individual lane packages | Public lane archives and batch summary |
| [Nyc exact output determinism](demos/nyc-exact-output-determinism/README.md) | Maps selected records to questions about exact-input, exact-output replay. | No standalone runnable package | Public index linking other evidence |

## Original numbered intake records

These root-level records are historical intake descriptions. They identify source artifacts and their particular evidence status; the record itself is not necessarily a runnable package. Some associated files are elsewhere in this repository or linked from the record. For records 07–10, the intake records say separate fresh-generation provenance was not established from the supplied files.

| Record | Subject | Runnable material and evidence |
| --- | --- | --- |
| [01](01_VerdictBridge_Master_Certificate_Intake_Record.txt) | VerdictBridge five-field hash comparison | Public intake and run artifacts; the intake does not itself provide a runnable evaluator. |
| [02](02_Global_Multirow_Coercivity_Master_Certificate_Intake_Record_v2.txt) | MathWise coercivity: packaging rejection and repair | Public intake; referenced verifier filename not found in this repository tree. |
| [03](03_Replayable_Damages_Mini_Demo_Master_Certificate_Intake_Record.txt) | Fixed synthetic damages arithmetic | Public intake; the two named source ZIPs were not found by their recorded filenames. |
| [04](04_JoyWise_Afterglow_Master_Certificate_Intake_Record.txt) | Exact text-file identity | Public intake and text files; no runnable evaluator identified. |
| [05](05_Erdos_124_Fixed_Certificate_Master_Certificate_Intake_Record.txt) | Erdős 124 fixed-case certificate | Public intake; named verifier not found in this repository tree. |
| [06](06_Erdos_390_Thirteen_Layer_Lower_Bound_Master_Certificate_Intake_Record.txt) | Erdős 390 partial lower-bound certificate | Public intake; named verifier not found in this repository tree. |
| [07](07_CleanWaterWise_Demo_Record.txt) | Synthetic water-quality routing | Public intake and archives; runnable contents not assessed here. |
| [08](08_FlightGate_Demo_Record.txt) | Synthetic flight routing | Public intake and archives; runnable contents not assessed here. |
| [09](09_StormWise_Demo_Record.txt) | Synthetic tornado-index calculation | Public intake and archives; runnable contents not assessed here. |
| [10](10_ChainGate_Demo_Record.txt) | Synthetic shipment release / hold rules | Public intake and archives; runnable contents not assessed here. |

[Return to the repository overview](README.md).
