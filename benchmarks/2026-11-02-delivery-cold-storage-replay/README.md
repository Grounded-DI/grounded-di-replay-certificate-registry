# Delivery-to-cold-storage synthetic replay

Six fictional shipments demonstrate receipt, destination, temperature-coverage and quantity checks. Of 19 planned units, **4 were accepted, 10 held, and 5 remain unknown** under the frozen rules. This is an accounting demonstration; its temperature thresholds are fictional assumptions, not medical or food-safety standards.

[Runnable replay ZIP](Cold_Storage_Replay.zip) · [Clean-extraction audit](audit.log) · [Frozen contract](CONTRACT.md)

Two fresh processes matched seven frozen JSON records by direct bytes and SHA-256. The separately implemented project checker passed both. Eight registered controls ran and passed; there were zero failures, errors, or skips. The clean-extraction audit repeated the checks. The altered-intermediate and coherently rehashed wrong-outcome controls test the checker, not an external receiver.

The checker shares the fixture, project specification, host and Python standard library with the producer; this is not external certification. Boundary 7 commits to boundaries 1–6 and is not independent verification. All times are fictional minutes relative to the beginning of the window; the example is not an emergency plan, real temperature assessment, production system, or proof of universal model determinism.

Replay ZIP SHA-256: `adb364a0a6a28c26bd1b5369231ca1b67321b2e3307cf38244b75e5e25d4d142`.
