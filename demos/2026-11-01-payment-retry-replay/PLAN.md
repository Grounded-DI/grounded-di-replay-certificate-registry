# Frozen public replay plan

Synthetic independent implementation, created for this publication; no private gate source. Python standard library; fixed time 100, expiry 200. Each case starts with a fresh in-memory gate and append-only JSONL file recorder. The gate consumes a request before calling the effect function; a lost response after the effect leaves UNKNOWN. Approval is a synthetic input, not identity authentication. Requests bind request ID, recipient, amount and expiry; same request ID is held after consumption. New IDs are separate requests. The local fixture models a trusted host and no concurrency or persistence.

Cases and expected outcomes:
- unprotected_loss: two invocations, two recorded effects.
- approved: one invocation, one effect, RELEASED.
- gated_loss: first invocation records effect then loses response; same ID retry HELD; one effect and recorder lookup finds it.
- changed_recipient and changed_amount: changed request fields denied, zero effects.
- missing_approval: denied, zero effects.
- expired: time 200 denied, zero effects.
- distinct_new_action: two individually approved IDs, two effects.
- duplicate_business_new_id: first ID records an effect and loses response; second approved ID with same recipient and amount also records an effect. Two effects are an expected limitation, not successful deduplication.

Fresh executions run this script in two distinct new directories. Canonical artifacts: results.json, events.json, effects.json. All three bytes must match exactly and SHA-256 must match. Files are compact sorted-key UTF-8 JSON with one LF. Each output includes observed facts, no volatile metadata. Source and this plan are SHA-256 bound in the verification record. No external network or provider behavior is tested. The recorder is separately read from a local JSONL file, not independently administered.
