# Water-quality comparison: reviewer walkthrough

A fictional community water system sends seven fictional arsenic records from a post-treatment entry point, except one deliberately labeled untreated-source sample. The operator wants a traceable comparison with EPA's published arsenic MCL of 0.010 mg/L, or 10 µg/L. This demonstration compares individual reported numbers only; it does not apply EPA's regulatory reporting rounding or determine compliance.

Open `frozen/SOURCE.md` for source links and context, `frozen/fixture.json` for the fictional records, and `evidence/run1/04_comparison.json` for outcomes. Example A is 8 µg/L, below the numerical reference; B is 0.012 mg/L, converted to 12 µg/L, above it. C is below its reporting limit, so the demo holds it rather than inventing a value. G is untreated source water and is held as outside this demo's selected context. These are not decisions about real water or health risk.

An operator can run `python3 -B src/producer.py frozen/fixture.json /tmp/water-new-run` and `python3 -B src/checker.py frozen/fixture.json /tmp/water-new-run` from the extracted package; the destination must be new. The six records provide the source identity, inputs, eligibility, comparison, report, and commitment. The checker recomputes against the supplied input; it does not independently authenticate the source or laboratory data. The commitment hashes the preceding records and is not a verifier.

A possible integration is between laboratory-result intake and a draft operator report. The buyer would still need to define accepted lab methods, sample identity and chain of custody, state-specific compliance requirements, rounding, confirmation and averaging, source updates, review and communication. No such integration is implemented.
