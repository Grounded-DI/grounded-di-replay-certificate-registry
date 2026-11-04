# Independent hand calculation, frozen before implementation
| Claim | Evidence / rule | Arithmetic in cents | Expected disposition |
|---|---|---|---|
| A | complete, covered | 40,000 − 10,000 = 30,000 ≤ 50,000 | ROUTE_PAYMENT, 30,000; COVERED_WITHIN_AUTHORITY |
| B | missing | no disposition calculation | HOLD, 0; EVIDENCE_MISSING |
| C | complete, excluded | no covered payment | DENY, 0; EXCLUDED_CAUSE |
| D | complete, covered | 60,000 − 10,000 = 50,000 = authority | ROUTE_PAYMENT, 50,000; COVERED_WITHIN_AUTHORITY |
| E | complete, covered | 60,001 − 10,000 = 50,001 > authority | HOLD, 0; AUTHORITY_EXCEEDED |
| F | evidence contradicts claimed cause | no disposition calculation | HOLD, 0; EVIDENCE_CONFLICT |

These values were derived directly from the fictional facts and rules, not by running the producer or checker. Provisional amounts exist only when evidence is OK and cause is covered; cap is applied after deductible.
