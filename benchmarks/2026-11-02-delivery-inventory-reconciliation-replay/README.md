# Delivery-to-inventory reconciliation replay

**PASS — synthetic, project-executed local demonstration.** Two fresh processes reproduced seven frozen canonical artifacts, and a clean-extraction audit repeated the checks.

[Reproducibility package](Delivery_Inventory_Replay.zip) · [Clean-extraction audit](audit.txt)

The fictional fixture follows five shipments. One matched order, shipment, receiver quantity, destination and inventory change, reconciling **10 supply cases**. The other four route to review: a two-case short receipt, a receiver record for the wrong destination, a missing receiver record, and duplicate records. Duplicate records are not summed; they are not proof of two deliveries.

| Boundary | Expected and observed SHA-256 | Run bytes |
| --- | --- | --- |
| 1 | `0ae07fc1781fbad01993114e3d11670fe4527d1293ff9e8be54823712add4bab` | Match |
| 2 | `ed95fac4848094c4d20041b543a6ce43699f3246e22fc75a80db0aecdda9aafe` | Match |
| 3 | `e8cc860142ea1b429d326c6e50a48e02e9095ef805bc7c51dc69543591151db1` | Match |
| 4 | `17d35acb3414727393f733ee109fb0b0bde16f6bca6e35768515c3e502e913ed` | Match |
| 5 | `ec8baf431a1461e631883044dd171ecbbbab89d5e9b93ad61278195a4ca0bc7d` | Match |
| 6 | `753f0e0920c6edd636f225650b3efe35de3453197846ee43f3f0b743791dd01d` | Match |
| 7 | `5f7c7cb3124697d0c7ae34a6114755ace41397efb5d3073c35b438df90dc6486` | Match |

Boundaries cover normalized orders, shipment bindings, receiver observations, record matching, reconciliation, final dispositions, and a commitment to boundaries 1–6. Boundary 7 is a commitment, not an independent verifier.

The separately implemented project checker recalculates all six stages and the commitment without importing producer code. It shares the fixture, specification, serialization, Python JSON and SHA-256 libraries, and host. The authorship and review are internal to the project.

Seven controls were registered and executed: **7 passed, 0 failed, 0 errors, 0 skips**. They exercise a changed shipment, wrong destination, missing receiver evidence, duplicate records, missing units, an altered intermediate artifact, and a wrong final record with a recomputed commitment. The package contains mutations, assertions, expected and observed outcomes, and raw process logs.

The final ZIP has SHA-256 `da7390a9d5a0a2b3de9ea027733da4d6d768e68b921d773a2fbd2a0ec3d6745b`. Its clean-extraction audit verified packaged checksums, repeated two fresh builds, ran both checker invocations and all controls, and compared all seven bytes and hashes against frozen expectations. No live destination or deployment was contacted.

The records are fictional and unauthenticated. A matching receipt is evidence within the fixture, not proof of a physical delivery. This is not an emergency plan, production readiness claim, external certification, exactly-once guarantee, or proof of universal model determinism.
