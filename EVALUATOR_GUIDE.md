# Evaluator walkthrough: expiry and policy

This walkthrough checks a synthetic local file-export example. It shows how an approved action is bound to a report, policy, scope, destination, and validity interval; how expiry or changed policy produces a refusal; and how a reviewer can rerun the recorded decisions and fresh controls.

## What you need

Python 3.9 or newer on macOS or a POSIX system with directory-descriptor operations and `O_NOFOLLOW`. The example uses the Python standard library. No model call, live service, third-party package, or real transaction is required. Use a separate checkout; the suite creates temporary altered copies and isolated synthetic output directories.

## Run the public example

```sh
git clone https://github.com/Grounded-DI/grounded-di-replay-certificate-registry.git
cd grounded-di-replay-certificate-registry
git checkout --detach ee3b0ae43faf25191c27bd5360f6377c83ebceeb
cd demos/2026-09-10-di2-expiry-policy-v1/source
sha256sum -c SHA256SUMS.txt
python3 -B verify.py
python3 -B acceptance.py
```

On macOS, use `shasum -a 256 -c SHA256SUMS.txt` in place of `sha256sum -c`. The pinned commit makes the walkthrough reproducible; later repository changes require a separately reviewed update.

## What to look for

- The checksum command reports `OK` for the listed files and exits zero.
- `verify.py` reports `PASS`, `case_count` 25, a fresh process, byte-identical canonical evidence, and replay SHA-256 `08f6750447a0f923d1b175a436f9ef03f98d0b50b755b52e276aed05bb410fe8`.
- `acceptance.py` reports `PASS`, 25 expected case checks, 10 boundary checks, and six rejected altered-copy controls. It separately performs a new real-clock expiry check and checks that the original source inventory is unchanged. The live timestamps are not expected to match prior runs.
- The expiry boundary is `issued_at <= execution_time < expires_at`: an action at the expiry instant is denied. Changing policy content without changing its version also invalidates the original policy binding in the recorded cases.

## Stop if a check fails

Stop and retain the command output if a checksum, process exit, replay identity, case count, boundary, altered-copy control, or original-inventory check fails. Do not report a pass from a stored result alone or use a failed or skipped check as evidence of a successful refusal.

## What the result covers

The example uses supplied synthetic authorization and policy snapshots, a local clock, and an isolated local export. The reference evaluator is a separate project implementation; it shares the specification and serialization utilities. The expiry check samples time before the write; it is not an atomic operating-system deadline. The self-issued, unsigned certificate records local project tests, not authenticated organizational approval, production deployment, external certification, or a live service result. See the [demonstration record](demos/2026-09-10-di2-expiry-policy-v1/README.md) for the complete contract and boundaries.

[Evidence index](EVIDENCE_INDEX.md) · [Evidence matrix](EVIDENCE_MATRIX.md) · [Repository overview](README.md)
