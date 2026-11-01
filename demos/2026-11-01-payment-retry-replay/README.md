# Payment Retry and Uncertain Outcome — Local Replay

A payment-like action is recorded locally, but its response is lost. What happens when the same request is retried, and when the same business payload arrives under a new request ID?

In two fresh local runs, this **new public demonstrator** produced identical canonical results for nine scenarios. It held a repeat of the same consumed request after one synthetic effect. A separately approved new ID with the same recipient and amount produced a second effect. The latter is an exposed boundary, not duplicate prevention.

- [Measured report](REPORT.md)
- [Frozen plan](PLAN.md)
- [Public demonstrator](demo.py)
- [Results](evidence/results.json) · [Dispatch events](evidence/events.json) · [Recorded effects](evidence/effects.json)
- [Replay verification](release-verification.json) · [Checksums](SHA256SUMS.txt)

Run `python3 -B demo.py /path/to/new-directory`, then compare `results.json`, `events.json` and `effects.json` with `evidence/` using byte comparison and SHA-256. The target directory must not exist. `sha256sum -c SHA256SUMS.txt` verifies the published files. Python standard library only.

The original private v0.3.1 gate exercise is a separate historical test. This newly written illustration does not execute that gate or establish an installed product capability. Data and effects are synthetic, and the local recorder is administered by the same test; no payment provider or account is used. The record is unsigned and self-issued.
