# VerdictBridge Demo 3 — selective punitive-control replay

**PASS — three fresh local executions; five-layer byte and SHA-256 agreement; invalid hearsay control refused before export.**

A newly implemented evaluator, operating on the same closed-world Lane v. Apex benchmark structure, produced the declared selective legal result reproducibly across three executions and correctly refused the inadmissible-hearsay control.

Punitive damages changes to `GRANT_SUMMARY_JUDGMENT`; strict liability, negligence, and compensatory damages remain `DENY_SUMMARY_JUDGMENT`. The overall motion becomes `GRANTED_IN_PART_DENIED_IN_PART`. The valid case remains VerdictReady and export-authorized. The Reed-dependent invalid candidate returns VerdictReady NO, export false, zero export-file opens, zero bytes written, and an empty output inventory.

## Read and download

- [PDF report — eight visually reviewed pages](package/VerdictBridge_Demo3_Report.pdf)
- [Complete public ZIP](VerdictBridge_Demo3_Public_v1.zip)
- [ZIP SHA-256 checksum](VerdictBridge_Demo3_Public_v1.zip.sha256.txt)
- [Standalone reproducibility specification](package/SPECIFICATION.md)
- [Detailed README and evidence index](package/README.md)
- [Unsigned local replay certificate](package/replay-certificate.json)
- [Measured verification](package/verification/verification-final.json)
- [Package checksum manifest](package/SHA256SUMS.txt)
- [New evaluator](package/source/evaluator.py) and [separate verifier](package/source/verify.py)

## Provenance and scope

**A. Original evidence:** five unchanged `Verdictbridge_demo-2` reference files, hash-pinned to registry commit `8472b48470b6c35a3ad2778f0819f36d4ddaef1b`.

**B. New evaluator:** newly implemented local Python code for this exact closed-world benchmark. The original folder supplied evidence, not executable engine source.

**C. Separate verifier:** an internal separate logic path, importing no evaluator code. It is not an external third-party attestation.

**D. Executions:** the original three fresh local executions are preserved with their receipts, canonical artifacts, and measured comparisons.

Operator-provided context: **Grounded DI OS via FastPath 6.1 Sol - Medium.** Measured computation uses the included local Python evaluator; the attribution is not provider metadata attestation.

No original engine execution, native VerdictBridge reproduction, universal model determinism, actual-jurisdiction legal validation, or external certification is claimed. The full conversational prompt is omitted; the standalone specification preserves the test contract. Public packaging changes leave canonical run artifacts and original references unchanged.

## Verify

Extract the public ZIP and enter its `VerdictBridge_Demo3_Public_v1` folder:

```sh
python3 -B source/verify_release.py
python3 -B source/acceptance.py
shasum -a 256 -c SHA256SUMS.txt
```

Core verification uses Python 3.9+ and the standard library on macOS/POSIX. PDF authoring additionally uses ReportLab.
