# OPR implementation review - 5 November 2026

## Verified from uploaded clone bundle

- Outer review bundle SHA-256 matched the supplied server value.
- The OPR is a custom, submitted DocType with **39 fields** (including layouts and hidden legacy fields), autoname `OFL-OPR-.YYYY.-.#####`, tracking enabled, rename disabled.
- The workflow has four states: Draft, Pending Approval, Approved, Paid. Five transitions authorize Requester, Approver, and Finance roles.
- Finance form script matches the backed-up client script, and was **enabled in the snapshot**. The snapshot also recorded the **clone** feature flag enabled. Production defaults MUST be OFF.
- Two Journal Entry custom reference fields exist. The source `controls.py` has checks for roles, amounts, account classification, source readiness, duplicates, payment proof and cancellation.
- Cancelled test GL entries are previously reported and verified by user outputs. This review does not independently access the live server.

## Deployment blockers / unresolved controls

1. Live `okavango_enhancements` source and hooks are not present in this package. Never replace production `hooks.py` with the clone version.
2. Source snapshot includes seven existing `Journal Entry` Property Setters, not demonstrated as OPR-owned. These are **EXCLUDED** from deployment manifest.
3. The clone's Payroll Statutory Return controllers are recovery placeholders; they are **EXCLUDED**. The clone's Server Scripts were intentionally switched off at clone creation; do not infer a production defect.
4. The source's Payment Method is recorded in remarks, but the backend validates Cash/Bank account classification without expressly matching the credit account type to the requested payment method. Finance should define an accepted policy for Cash, Bank Transfer and Mobile Money.
5. The OPR can be Approved while its accounting_status is Cancelled and JE link blank; with feature ON, another JE may be created. Decide the reissue/correction approval policy and audit treatment.
6. Server-side tests of unauthorized manipulation of Finance fields (`paid_amount`, `paid_on`, `payment_proof`, `finance_notes`) and prohibited state transitions through direct API are still needed, beyond UI role restrictions.
7. Submitted JE credits cash/bank before the separate Paid step. Finance must confirm posting point aligns with actual disbursement; this has direct balance impact.
8. Legacy fields (hidden `amount`, `payment_category`, etc.) coexist with originals and may have stale values. Verify all reports and downstream code read `requested_amount` and `category`.
9. Individual user-role assignments are not in the configuration snapshot and must be assigned through approved live access provisioning.
10. The 39-field schema includes DocType layouts and the original fields; do not import a second new 39-field DocType into a site containing an existing OPR without a field-by-field migration review.
11. `controls.py` was reviewed statically; compatibility with live site's Frappe/ERPNext version, hooks, account restrictions and all related apps is unverified.

## Approval gate

This is a **production-readiness candidate**, not an authorized automatic production installer. Obtain a read-only live preflight and a verified source backup, resolve critical policy/security gaps, complete supplier/statutory regression tests on clone, and get Finance + Operations sign-off before any live write.
