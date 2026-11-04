# Inspecting a fictional claims decision

A claim can move toward payment, review, or denial for different reasons. This local demonstration models a fictional equipment policy and shows the inputs, rules, calculations and reason for each route before any payment instruction exists.

The frozen sample has six claims. One routine covered loss routes for 300 dollars, another reaches a 500-dollar authority limit exactly, a one-cent-higher provisional amount is held, missing and contradictory evidence produce holds, and an excluded cause is denied. Every number and record is invented.

A buyer can inspect the original input, rule specification and hand-calculated expected results, run the producer in fresh processes, compare seven records by bytes and hash, and run a separately implemented checker. The first six records cover inputs, coverage classification, evidence checks, calculation and authority, decision, and synthetic disposition. The seventh commits to the first six; it is not an independent verifier. The checker recomputes the records from the input it is given. In local tests it rejected altered records, including an altered decision with a newly computed commitment, when checked against the frozen input.

A possible integration point is after a claims system assembles a proposed decision and before it sends a payment or denial action. An adapter could capture the source data and policy version, call a decision service, and present the decision and evidence for authorized review. That integration is proposed; it was not built or tested here.

A buyer would need to define policy language and versions, acceptable evidence, identity and authority, data provenance, review and appeal procedures, applicable legal obligations, security, integration and deployment controls. The sample has no external authentication, real claim data, live connector, human approval workflow, or payment function. The checker trusts its supplied input; if all inputs and outputs are replaced consistently, it cannot establish which version was authorized. Results are for the included synthetic cases and environment only.
