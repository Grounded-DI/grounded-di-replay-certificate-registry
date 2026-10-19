# Additional Legal Evidence Replay Demonstrations — 2026-10-19

This batch adds three distinct closed-world legal evidence workflows to the Grounded DI replay registry. Each lane was executed twice from the preserved canonical input, checked through a separate verifier, and subjected to an altered-input or tamper control.

| Lane | Canonical executions | Replay identity | Verifier | Tamper controls | Canonical record SHA-256 | Archive SHA-256 |
|---|---:|---|---|---|---|---|
| [BriefWise — Authority-Proposition Replay](briefwise-authority-proposition/README.md) | 2 | PASS | PASS | PASS | `3cef3984a39cf26c1323e0a4682ebb61f5feab0de85d1de435294291588d051c` | `c4f4eb3e9b7d3ffc625644a294f6ea744f5a1ea9618b79eb73cdeb8d2b113772` |
| [DepoBot — Testimony-Contradiction Replay](depobot-testimony-contradiction/README.md) | 2 | PASS | PASS | PASS | `2020e012f9010b6bef2ffd73d722d8528b54d1ff6545654ded406c04e7188f4a` | `704a12b3ee544d88e1e5d2122168d03b15ad516b24c1679a176b232cf674f66a` |
| [PIDBot — Product/Exposure Evidence Replay](pidbot-product-exposure/README.md) | 2 | PASS | PASS | PASS | `b4c8c887b17c38c6a77c044fbef8d0ac24fe906e9ec371e1ff1a906824654427` | `bf27d41c6ffeb798de76254716206e2b491bd8b9d8d010535fc4af294858bc24` |

## Scope

All records are synthetic closed-world fixtures. The results establish only the recorded behavior of the supplied source, inputs, specification, and environment. They do not establish independent fresh-generation provenance, external verification, legal correctness, filing readiness, real-world product identification, exposure, dose, causation, liability, or deployment.
