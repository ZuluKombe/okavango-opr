"""Read-only live compatibility inventory for Okavango OPR.

Run inside bench --site <SITE> console:
    exec(open('/absolute/path/checks/production_preflight.py').read())
    run_opr_preflight()

No writes, schema migration, config changes, or commit.
"""
import json
import frappe

ROLE_NAMES = ('Operational Payment Requester', 'Operational Payment Approver', 'Operational Payment Finance')
JE_FIELDS = ('custom_operational_payment_request', 'custom_customer_order_reference')

def run_opr_preflight():
    site = str(getattr(frappe.local, 'site', ''))
    installed = frappe.get_installed_apps()
    has_opr = bool(frappe.db.exists('DocType', 'Operational Payment Request'))
    existing_workflows = frappe.get_all('Workflow', filters={'document_type':'Operational Payment Request'}, fields=['name','is_active'])
    scripts = frappe.get_all('Client Script', filters={'dt':'Operational Payment Request'}, fields=['name','enabled'])
    je_meta = frappe.get_meta('Journal Entry')
    hooks = frappe.get_hooks('doc_events') or {}
    je_hooks = hooks.get('Journal Entry', {}) or {}
    opr_hooks = hooks.get('Operational Payment Request', {}) or {}
    blockers=[]
    if 'okavango_enhancements' not in installed:
        blockers.append('Existing custom app okavango_enhancements not installed')
    if has_opr:
        blockers.append('OPR already exists: reconcile fields and records; do not blindly import')
    if existing_workflows:
        blockers.append('Existing OPR workflows require manual conflict review')
    if scripts:
        blockers.append('Existing OPR Client Scripts require manual conflict review')
    for name in JE_FIELDS:
        if je_meta.has_field(name):
            blockers.append('Existing JE field '+name+' requires type/options/permission diff')
    if any(je_hooks.values()):
        blockers.append('Existing Journal Entry hooks must be MERGED, never overwritten')
    report={
        'site':site,
        'installed_apps':installed,
        'existing_opr':has_opr,
        'opr_record_count': frappe.db.count('Operational Payment Request') if has_opr else None,
        'opr_workflows':existing_workflows,
        'opr_client_scripts':scripts,
        'opr_roles':{role:bool(frappe.db.exists('Role', role)) for role in ROLE_NAMES},
        'je_custom_reference_fields':{name:bool(je_meta.has_field(name)) for name in JE_FIELDS},
        'je_doc_event_hooks':je_hooks,
        'opr_doc_event_hooks':opr_hooks,
        'server_script_enabled_site':frappe.conf.get('server_script_enabled',0),
        'server_script_enabled_bench':frappe.get_common_site_config().get('server_script_enabled',0),
        'statutory_je_reference_field':bool(je_meta.has_field('custom_payroll_statutory_return')),
        'opr_expense_feature_flag':frappe.conf.get('okavango_opr_expense_enabled',0),
        'needs_manual_live_diff':blockers,
        'no_changes_performed':True,
    }
    print(json.dumps(report, indent=2, default=str))
    return report
