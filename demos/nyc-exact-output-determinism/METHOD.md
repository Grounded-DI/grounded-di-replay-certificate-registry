# Common Replay and Controlled-Execution Method

## Method statement

The registry’s recurring method can be represented as:

```text
declared input, policy, configuration, and state
  → canonical record
  → explicit evaluation
  → decision or refusal
  → controlled output boundary
  → receipt, hash, or audit trace
  → replay or verification
```

This is an architectural pattern expressed through different evidence instances. It is not a claim that every artifact uses the same evaluator, rule language, serializer, or runtime.

## Shared invariants

### 1. Input and governing state are made explicit

The selected records preserve or bind the relevant input, evidence, policy, configuration, destination, scope, validity interval, or mathematical certificate. The exact fields vary by domain.

### 2. Evaluation is rule-governed

The result is derived through explicit predicates, thresholds, state transitions, arithmetic, or certificate checks. Domain logic remains visible rather than being hidden behind a common label.

### 3. The output state is controlled

Depending on the evidence instance, the controlled result is an authorized export, refusal, hold, FLY/NO_FLY decision, legal disposition, mathematical certificate status, or preserved uncertainty state.

### 4. Output identity is preserved

The registry uses canonical records, fixed archive metadata, manifests, receipts, replay identities, and SHA-256 hashes. These mechanisms make the relevant bytes and state inspectable.

### 5. Replay or verification is performed

Evidence ranges from three fresh evaluator processes and a separate verifier in VerdictBridge Demo 3, to a separate reference evaluator in Expiry and Policy Replay, packaged verifiers in the routing records, and clean-room mathematical verification in Global Multirow Coercivity.

## What varies by evidence instance

| Evidence instance | Domain-specific layer | Serialization/output detail |
|---|---|---|
| VerdictBridge Demo 3 | Finite legal facts, admissibility predicates, gate matrix, selective dispositions | Sorted compact JSON, canonical CSV, final-newline assessment text, fixed ZIP metadata |
| Expiry and Policy Replay | Authorization, validity interval, full policy hash, destination, export gate | `DI2-ASCII-JSON-LF-1`; canonical replay identity and saved exports |
| ChainGate | Shipment temperature, seal, document, variance, and delay rules | Exact decimal values, fixed ZIP package, audit-linked decisions |
| FlightGate | Mission thresholds, required fields, configuration validation, FLY/NO_FLY routing | Manifest-bound synthetic mission package |
| Global Multirow Coercivity | Exact rational certificate, clean-room source packet, mathematical verifier | Manifested certificate and verification packets; packaging repair preserved as history |

## Evidence vocabulary

- **Fresh-process replay:** a new process evaluates the preserved input or history.
- **Fresh verifier execution:** a supplied verifier is run again against saved artifacts.
- **Byte identity:** compared files or archives contain exactly the same bytes.
- **Hash agreement:** SHA-256 values match the recorded or compared artifacts.
- **Separate verification:** a distinct internal checker or reference path tests the result. It is not automatically third-party validation.
- **Controlled divergence:** a declared material input or configuration change produces a changed result under the same control pattern.
- **Boundary result:** the system routes to authorization, refusal, hold, uncertainty, or another explicit state before or at the controlled output boundary.

## Layer distinction

Model-level stochastic generation and system-level controlled/replayable execution are different layers. The NYC evidence track measures the latter: the reproducibility of governed decision records and output artifacts under declared conditions. Where a model is mentioned in an artifact’s provenance, that attribution remains separate from the measured local evaluator or verifier unless the artifact expressly establishes otherwise.
