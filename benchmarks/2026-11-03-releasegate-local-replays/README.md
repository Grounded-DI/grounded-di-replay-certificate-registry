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

## Additional local replays — November 3, 2026

Four further project-executed replays used the same frozen package and followed the same synthetic process and checks described above. For each, both processes matched all seven boundaries by bytes and SHA-256; both checkers passed; and all 12 registered tests passed, including 11 negative controls, with no failures, errors or skips. The synthetic promoted file matched the candidate. The private evidence archives were inspected during publication review.

| Run time (Eastern) | Private evidence ZIP SHA-256 |
| --- | --- |
| 7:42 a.m. | `78090cad80c4f314e437d659659f8f87b44a67196c129f54d1fefd3d0aeb66dc` |
| 8:48 a.m. | `a11fe0185a870ca06796024f54ee8d267dab4a450f6351153d5342d6c1ceb840` |
| 9:49 a.m. | `5e7a66a1c9bd003078f39f0931c5a5b11221c746dc9ed3add13e146d3a8f5bf9` |
| 10:51 a.m. | `76b50163adc2854f20490258968910a24da2672eaecd5a995d549182a68e5e31` |

## Further local replays — November 3, 2026

Eight further project-executed synthetic replays used the same frozen package and checks described above. For each, two fresh processes matched all seven boundaries by bytes and SHA-256; both project checkers passed; and all 12 registered tests passed, including 11 negative controls, with zero failures, errors or skips. The synthetic promoted file matched the candidate. Private evidence archives were inspected during publication review. These are historical runs, not new executions during the review.

| Run time (Eastern) | Private evidence ZIP SHA-256 |
| --- | --- |
| 11:51 a.m. | `a9341a645b151e4187dd23a520b3bc60a1f49912960f58adbb43a2b22dab5110` |
| 12:44 p.m. | `148be651b67139a4122c535972cb55ea659d6740fe6e10ea36cdbf4f9a9b8dac` |
| 1:50 p.m. | `eb9402a0b0911c4c3b1a4a2140ab144146a61cfcbeb7d89aac0178e9333b8efd` |
| 2:48 p.m. | `994deb31462bc696a2a5ab98c569b4cce1a1bfa37db133018609b48f3afa4e42` |
| 3:49 p.m. | `c39541653dd284001fa5740f2993058e24a1f9be73b484eb2eeb0626b6b86fd9` |
| 4:49 p.m. | `20fafe9745f4a096feb537dbe0c488f5d5baffd901b0d51905cd4773991ab279` |
| 5:48 p.m. | `46d627f30650290935be122a9bb78def6b599242442ddac788b563f4febbcab6` |
| 6:48 p.m. | `527756d475235b87575fcb3631db275124b94d1b628cfa3e308f94eb9badf1f4` |
