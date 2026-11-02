# Flood to delivery: alternate route replay

Synthetic network D–A–B: the direct road D–B is closed at 40 cm, while D–A and A–B are open. Ten units are allocated in alphabetical order: A receives six, B receives four through A; one unit of demand remains unmet. This is not a real flood prediction or emergency plan.

[Reproducibility evidence](Flood_Delivery_Evidence.zip) · [Clean extraction output](audit.log)

Evidence ZIP SHA-256: `d9e393954b84fbb72418de6917a72655c1a3833a7940ef9ed9442692587ba015`. It contains the runnable replay ZIP and clean extraction output.

Two fresh executions matched all seven frozen files directly by bytes and SHA-256. Both project checker runs passed. Seven controls were registered and executed: 7 passed, 0 failed, 0 errors, 0 skipped; the clean extraction repeated them. The initial capacity control was strengthened after its first execution; both versions are preserved. The intermediate-tamper and rehashed-wrong-result controls test the separate checker, not a live downstream delivery action.

The checker is separately implemented but shares the fixture, specification, Python standard library and host. The final boundary is a commitment to the other six, not independent verification. This is project-local evidence, not external certification, production readiness, or universal model determinism.
