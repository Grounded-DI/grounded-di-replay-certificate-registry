# Synthetic insurance claims decision replay

Grounded DI LLC — local synthetic demonstration, November 4, 2026.

This demonstration routes fictional equipment damage claims for payment, review, or denial under an invented policy. No real claim, coverage decision, denial, insurance system, or payment is involved. See [buyer brief](BUYER_BRIEF.md), [report and replay instructions](REPORT.md), [frozen rules](frozen/SPEC.md), [fixture](frozen/fixture.json), [hand-calculated outcomes](frozen/EXPECTED.md), and [test results](evidence/test_results.json).

Two fresh producer runs generated matching bytes at all seven boundaries; the separate checker accepted both. The test runner recorded 53 passes, zero failures and zero skips. It independently recomputes outputs from the supplied inputs, while sharing the stated schema and rules. The seventh artifact commits to the six preceding artifacts; it is not an independent verifier. Hashes do not establish source authenticity, completeness or truth. The checker cannot identify a coherent replacement of both its input and outputs. This demonstration is not a production system or a statement of compliance or certification.

Requires Python 3.11+ and standard library. Test commands and the archived environment appear in REPORT.md. Replays use new output directories. For preservation, make a copy before running the test runner: it writes its result JSON inside evidence/.
