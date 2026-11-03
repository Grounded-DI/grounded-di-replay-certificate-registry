# ReleaseGate synthetic local replays — November 3, 2026

Six project-executed replays of the [ReleaseGate promotion demonstration](../2026-11-01-releasegate-promotion-replay/README.md) used the frozen source package with SHA-256 `e70243b61d550d414b6f1f591eb1dca2d3765718dfb99fc720ac1e2bdd0f48c5`.

Each replay used two fresh local processes and separate output directories. The seven canonical artifacts matched each other and preserved references by direct byte comparison and SHA-256. Both project checker invocations passed. All 12 registered tests passed: one baseline and 11 negative controls, with zero failures, errors, or skips. The baseline decision was ELIGIBLE and one synthetic promotion file matched the candidate bytes. Frozen-input and package checksum checks passed.

| Run time (Eastern) | Private evidence ZIP SHA-256 |
| --- | --- |
| 1:47 a.m. | `18933c7ebd8a8a65edfc56b487b711fb2efdd47a17a1ff1eb33b5a74db015420` |
| 2:53 a.m. | `7e223612bae3f7238490942a8834d754ef66e3e55c7180341e640e19f3cf4119` |
| 3:43 a.m. | `a4f4285337618de4b51ae7f1823a4a4db34d0d29c2b6eea4770951743b48f505` |
| 4:53 a.m. | `e9de0744b0aaba265b7ac8d757dace392cc6b2d152f9e90efbab57f66614caf8` |
| 5:44 a.m. | `7c61c02725044590534503fac59433ee5ee7ebdaab73a302dead3ced85493e78` |
| 6:51 a.m. | `052245828d957c767c692fb9e79e8f803314eec64746d58594970827e32e5abc` |

The evidence archives are privately retained and are not published here. The outputs and logs in those archives were reviewed for this record; the above are historical executions, not new runs during publication review.

The seven boundaries record request, artifact, tests, approval, policy, decision, and commitment. The seventh commits to the preceding six and is not an independent verification. The two processes share a host and software dependencies; the separately implemented project checker shares the specification, fixtures, and standard libraries. These synthetic local results do not establish production stability, universal model determinism, or third-party certification.
