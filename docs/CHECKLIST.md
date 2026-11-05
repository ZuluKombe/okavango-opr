# Controlled implementation checklist

- [ ] Read-only production preflight report reviewed
- [ ] Production `okavango_enhancements` app source and hooks backed up / diffed
- [ ] Existing JE role permissions, supplier and statutory hooks preserved
- [ ] Reconcile existing OPR DocType/workflow/custom field names with candidate
- [ ] Resolve Finance-only server API mutation and workflow transition tests
- [ ] Finance approves accounting date, cash/bank selection and payment evidence policy
- [ ] Confirm live server-script configuration independently of clone setting
- [ ] Develop idempotent, conflict-aborting OPR-only installer with rollback
- [ ] Exercise production installer on isolated staging copy of live ERP
- [ ] Regression: OPR, Purchase Invoice, Payment Entry, supplier JE, statutory return JE
- [ ] Record deployment approval by Finance and Operations
- [ ] Activate on production for a narrowly controlled pilot only, after sign-off
