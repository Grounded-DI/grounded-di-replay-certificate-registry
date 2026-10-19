# Integrated Legal Evidence Chain Replay — Measured Report

## Scope

This package is one connected, closed-world synthetic product-liability
matter. Synthetic authorities, transcript entries, exhibits, products,
entities, worksites, evidence records, and outcomes are test fixtures.
Nothing in this report is a claim about a real case, real law, real product,
real exposure, real dose, real causation, or real liability.

## Execution result

- Fresh chain executions: **2**
- Stage subprocesses per execution: **4**
- Total stage subprocess executions: **8**
- BriefWise executions: **2**
- DepoBot executions: **2**
- PIDBot executions: **2**
- VerdictBridge executions: **2**
- Stage-level replay identity: **PASS**
- Final-chain replay identity: **PASS**
- Independent evaluator: **PASS**
- Control suite: **PASS**
- Final disposition: **`INSUFFICIENT`**
- Verdict-ready: **false**
- Observed replay divergence: **none**
- Baseline record mismatches: **none**

The final synthetic recommendation is to reserve a final sufficiency ruling
because the closed-world record has unresolved authority and evidentiary gaps.
That recommendation is a bounded inference from the fixture, not a legal
conclusion about a real matter.

## Stage results

### BriefWise

The authority map binds P-001 and P-002 to supplied synthetic holdings. P-003
is an inference requiring factual application. P-004 references a missing
synthetic authority and remains unresolved. Authority binding does not prove
facts or establish exposure, dose, causation, or liability.

Canonical stage SHA-256:

```text
9334b37f68ba58b87443ab67defc2e668e2de1582cf7b3d61063bac25e03c89c
```

### DepoBot

The testimony matrix preserves speaker, question, answer, page/line, exhibit,
and source fragment. C-001 records a direct contradiction by Witness A about
the same repair at North Plant in 2014. C-002 remains ambiguity, C-004 remains
a characterized unanswered question, and C-005 remains an omission/missing
foundation. C-003 is a negative control and is not classified as a
contradiction.

Canonical stage SHA-256:

```text
c22a001b36e01faec8a982c38b75769b042beb5eb003a7c61b00da89e7ded71b
```

### PIDBot

The product/manufacturer record matches Model Z-14 under the disclosed rule.
The gasket component is not tied to a component specification or supplier
record. Witness belief does not establish material content. Exposure is not
upgraded to dose, causation, or liability. Dose is unquantified; the synthetic
record supplies no causation opinion; complete legal liability remains
unsupported.

Canonical stage SHA-256:

```text
74dff06e53ef73d0e2de7b6df840690a6127a0aa6180213262ed418eabb5536b
```

### VerdictBridge

VerdictBridge preserved the contradiction, PIDBot uncertainty, and the
separation between product, material, exposure, dose, causation, and liability.
The final result is `INSUFFICIENT`, with `verdict_ready: false`. The final chain
hash is:

```text
9c68fd56872beac428bb8feeb240b93f340aa4a8d4f407b5802d665fd645d325
```

## Chain controls

The control record covers every required alteration:

- removed authority;
- altered deposition answer;
- altered transcript page/line binding;
- replaced product identifier;
- added unsupported material assertion;
- injected causation override;
- altered an intermediate stage after downstream generation; and
- manually changed the final output to `VERDICT_READY`.

The first six altered-input cases produced changed or refused results. The two
post-generation tamper cases caused the independent evaluator to fail. The
unsupported material assertion and manual causation override were recorded as
rejected rather than allowed to upgrade downstream status.

## Replay identity and provenance limits

The stage records and final chain are byte-stable under the same local fixture,
serialization rules, scripts, and environment. This demonstrates local replay
identity for this package. It does not establish independent fresh-generation
provenance, external verification, universal determinism, or production
readiness.

## Explicit non-claims

This package does not claim:

- real legal correctness;
- filing readiness;
- real product identification;
- real exposure, dose, causation, or liability;
- independent fresh-generation provenance;
- external verification; or
- production deployment.
