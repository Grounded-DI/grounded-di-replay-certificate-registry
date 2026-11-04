# Synthetic arsenic comparison replay

Read REPORT.md and BUYER_WALKTHROUGH.md. Requires Python 3.11+ and standard library. From this directory, choose two nonexistent output directories:

    python3 -B src/producer.py frozen/fixture.json /tmp/water-replay-a
    python3 -B src/producer.py frozen/fixture.json /tmp/water-replay-b
    python3 -B src/checker.py frozen/fixture.json /tmp/water-replay-a
    python3 -B src/checker.py frozen/fixture.json /tmp/water-replay-b
    python3 -B src/test_cases.py

The suite compares the two archived evidence runs and writes evidence/test_results.json; preserve the archive or work on a copy. Output is a numerical comparison, not a compliance, safety, or health-risk determination.

The generated report was corrected after the publication audit; see audit/PUBLICATION_AUDIT.md and frozen/REPORT_REVISION.md.

    python3 -B src/test_report_revision.py
