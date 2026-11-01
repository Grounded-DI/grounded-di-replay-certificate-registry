# Technical replay record

## Source binding

The original archive `GroundedDI_SevenHash_ReplayBenchmark_v1_20261019.zip` matched SHA-256 `497614c00216d7fe86886afdfd93aa7c08a5d65a590c38dd8a78e5380d80fa98`. Its detached unsigned receipt matched the delivery verifier across 116 members. The receipt's own SHA-256 and frozen execution-contract identity are recorded in [verification.json](verification.json). The project record is unsigned, so byte identity does not establish independent authorship or certification.

The prior November 1 diagnostic was inspected. Its hold cited changed Python/zlib versions, unavailable historical evidence ZIPs, and an initial process launch that did not execute a target command because its working directory was absent. The frozen environment document records the original versions; the execution contract specifies artifact bytes and verification rather than prescribing those exact runtime versions. The separate strict and closure evidence ZIPs were not found in the available local archive search or the Library title search; the frozen original, detached receipt, and prior diagnostic were available. This replay does not attest the missing archives.

## Execution and comparison

The package was extracted twice: one copy for execution and a clean copy for packaging. Before tests, two separate `pack_release.py` processes reconstructed the original 116-member payload. Both ZIPs matched each other and the original by direct byte comparison and SHA-256. The original receipt is detached and was not inserted into the repackaged ZIPs.

`replay.py` launched two fresh benchmark processes and separately ran the project's mathematical verifier against each output; both verifier processes reported PASS with 49 checks. It compared all eight output files directly against each other and the published baseline. The five artifact hashes and Merkle root are the six computational boundaries. The seventh is historical-payload ZIP identity. Each expected and observed value is listed in [verification.json](verification.json).

The independent mathematical verifier was also run on the original bundled A and B artifacts: both passed 48 recorded checks. The original 31-method unit suite passed and the 14 negative controls passed, with the baseline left unchanged. These are separate test counts. The verifier uses a distinct implementation in the same project and host; it is not unaffiliated review.

## Commands and retained evidence

The retained private evidence records actual argument vectors, working directories, UTC start times, exit codes, standard output and standard error, fresh outputs, and control observations. The eight command categories were delivery verification, packaging A and B, original mathematical verification A and B, unit discovery, fresh replay, and negative controls; all exited zero. Raw logs contain local paths and are retained outside this public repository. The private evidence archive SHA-256 appears in the verification record; the archive is not offered as a repository download.

No historical artifact was altered. No new full-delivery ZIP identity is claimed for the fresh computational results or their live process receipts. SHA-256 matches show byte identity at the specified boundaries; domain checks and controls provide separately scoped evidence about the computation.
