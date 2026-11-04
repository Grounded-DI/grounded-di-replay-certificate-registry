# Nitrate threshold screening — local replay (corrected v2)

Grounded DI LLC · November 4, 2026

A small Python demonstration compares fictional sample values with the U.S. EPA National Primary Drinking Water Regulations table value for nitrate measured as nitrogen: 10 mg/L. [EPA source](https://www.epa.gov/ground-water-and-drinking-water/national-primary-drinking-water-regulations). `source_excerpt.txt` is a locally prepared excerpt of the table entry, not downloaded EPA page bytes. No real water samples are used.

| Sample | Fictional value | Demonstration outcome |
| --- | --- | --- |
| S1 | 4.2 mg/L as N | AT_OR_BELOW |
| S2 | 10 mg/L as N | AT_OR_BELOW |
| S3 | 10.1 mg/L as N | REVIEW_ABOVE |
| S4 | 12 mg/L nitrate | HOLD: reporting basis unsupported |

These classifications are a narrow numeric comparison, not a regulatory compliance determination, assessment of drinking-water safety, or advice. The EPA standards apply to public water systems; actual compliance involves applicable monitoring and other rules. No conversion between reporting bases is implemented.

## Review finding and correction

The initial private v1 demo produced reproducible classifications, but a later audit found its checker accepted the old result when S1 was changed from 4.2 to 4.3, because both values produced the same classification. V1 output did not bind the exact input bytes. That finding is retained in private audit evidence; v1 was not replaced.

In this v2 correction, the producer records the SHA-256 of the exact input bytes it parses. The checker separately hashes its supplied input and rejects a mismatch. A regression test checks the same-category substitution. This detects a changed input against a retained result; it does not authenticate the source or prevent an actor who can replace both input and result from making a new consistent record.

Two fresh local v2 processes matched the independently frozen expected result byte-for-byte and by SHA-256. Both checker invocations passed. The registered suite executed 12 tests: 12 passed, zero failures, errors, or skips. The expected result SHA-256 is `943deeac75128f82d2d5d4757eb34c3cc5242a7bef9cb1f66d2b1e309fd22c59`. The initial v1 suite passed 11 tests but did not test the later input-substitution finding; the v2 suite adds that control.

The source excerpt and its selected local pin can be changed together; this demo does not establish source selection authority, authenticate a laboratory result, or verify chain of custody. The producer and separate checker share Python, configuration and assumptions. The two processes ran on one host; this is not production validation or external certification.

## Reproduce

Requires Python 3 and its standard library. From this directory:

```sh
sha256sum -c SHA256SUMS.txt
workdir=$(mktemp -d)
python3 producer.py --out "$workdir/a.json"
python3 producer.py --out "$workdir/b.json"
cmp "$workdir/a.json" "$workdir/b.json"
cmp "$workdir/a.json" expected/result.json
sha256sum "$workdir/a.json" "$workdir/b.json" expected/result.json
python3 checker.py --out "$workdir/a.json"
python3 checker.py --out "$workdir/b.json"
python3 -B -m unittest -v test_demo
```

The frozen decisions, data format and trust boundaries are specified in [CONTRACT.md](CONTRACT.md). Expected input and result digests are in [FREEZE_V2.json](FREEZE_V2.json). The project authored both implementations; the checker is a separate code path, not an unaffiliated review.
