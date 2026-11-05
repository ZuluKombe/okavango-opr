# Okavango Operational Payment Request - Production Readiness Candidate

**STATUS: REVIEW ONLY - DO NOT RUN AS A PRODUCTION INSTALLER**

Source: user-uploaded, integrity-verified clone review bundle dated 2026-11-05.

Contents:
- `candidate_module/operational_payment/controls.py`: tested clone backend source, unmodified.
- `candidate_module/operational_payment/client_script.js`: tested clone Finance button source, unmodified.
- `schema/opr_owned_manifest.json`: whitelisted OPR-specific definition, roles, workflow and two JE custom fields, stripped of clone owner metadata and unrelated JE Property Setters.
- `checks/production_preflight.py`: READ ONLY; prints live compatibility inventory without changing any records.
- `docs/REVIEW_FINDINGS.md`: confirmed implementation points and unresolved deployment blockers.

## How to run the read-only production preflight (no installation)

1. Obtain approval to inspect the live ERPNext server and take a verified backup first.
2. Copy only `checks/production_preflight.py` to a controlled read-only working directory on that server. Do not overwrite any app code.
3. In the live server terminal, open `bench --site <ACTUAL_SITE> console`. At the Python `In [1]:` prompt, run:

       exec(open('/absolute/path/checks/production_preflight.py').read())
       run_opr_preflight()

4. Redact site-specific details as appropriate before sharing results. `run_opr_preflight` is read-only; it performs no schema or record writes.
5. Compare live hooks, server script policy, JE customizations and installed app versions before writing a migration.

## Deployment rules

- Do not copy this candidate's `controls.py` into live before a code review and direct API permission tests.
- Do not copy an entire clone `hooks.py` or recovered DocTypes into production.
- Do not import the supplied Property Setters automatically.
- Create an idempotent installer only after live preflight; abort on conflicts, do not overwrite existing metadata blindly.
- Initial production feature flag: `okavango_opr_expense_enabled=0`.
- Initial production Finance Client Script: `enabled=0`.
- No migration/restart or accounting posting is authorized by this package.
