# Flood-to-delivery synthetic replay

**PASS — project-executed local replay, November 2, 2026.** A fictional depot has three direct roads: east to a clinic, north to a school, and west to a shelter. A road closes when water reaches its stated threshold. In the frozen fixture, west is closed. With eight supply units and clinic-first allocation, five units reach the clinic, three reach the school, and none reach the shelter; ten units of demand remain unmet.

[Runnable reproducibility package](Flood_Depot_Replay.zip) · [Clean-extraction audit](audit.txt)

Package SHA-256: `412eca5b40ecc8b567c419fd5e4311a08c9ccd789924626bcd838d9601036372`.

Two fresh processes produced seven byte-identical JSON artifacts, each matching independently prepared frozen expected hashes. Boundaries cover normalized inputs, road flood conditions, closure decisions, routes, allocations, outcome, and a commitment to the preceding six. The seventh is a commitment, not an independent verifier. The frozen hashes and direct comparisons are in the package.

The separately implemented checker recalculates all outputs from the fixture; it does not import the producer. It shares the project specification, fixture, host, Python JSON, and SHA-256 libraries. Both checker invocations passed. Seven controls were registered and executed: **7 passed, 0 failed, 0 errors, 0 skips**. They cover road closure, an unreachable destination, capacity, missing units, a legitimate input change, altered intermediate output, and a wrong final record with its commitment recomputed. Clean extraction of the final package repeated checksums, both executions, both checker runs, the seven controls, and byte and hash comparisons successfully. Initial command output was transcribed from the captured tool response; the package says so. The archived audit log records the first extraction audit; the linked audit records the final package audit.

This is a fictional, fixed local example, not a real flood forecast, emergency plan, external certification, production system, or proof of universal model determinism.
