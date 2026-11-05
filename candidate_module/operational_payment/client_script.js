// ERPNext v15 clone. The user's ORIGINAL 22 OPR fields are the source of truth.
// Uses already-installed okavango_enhancements server methods; no new app path.
// Do not activate until Finance permission and API tests pass.
frappe.ui.form.on('Operational Payment Request', {
    refresh(frm) {
        if (frm.is_new() || frm.doc.docstatus !== 1 ||
            frm.doc.workflow_state !== 'Approved') return;
        if (!(frappe.user.has_role('Operational Payment Finance') ||
              frappe.session.user === 'Administrator')) return;
        const source_name = frm.doc.name;
        frappe.call({
            method: 'okavango_enhancements.operational_payment.controls.get_button_state',
            args: { source_name },
            callback(r) {
                if (frm.doc.name !== source_name || !r.message) return;
                if (r.message.existing_name) {
                    frm.add_custom_button(__('Open Expense Entry'), () => {
                        frappe.set_route('Form', 'Journal Entry', r.message.existing_name);
                    });
                    return;
                }
                if (!r.message.allowed) return;
                frm.add_custom_button(__('Create Expense Entry'), () => {
                    frappe.call({
                        method: 'okavango_enhancements.operational_payment.controls.get_journal_entry_prefill',
                        args: { source_name },
                        freeze: true,
                        freeze_message: __('Preparing expense entry...'),
                        callback(result) {
                            if (!result.message) return;
                            const data = result.message;
                            frappe.new_doc('Journal Entry', {
                                company: data.header.company,
                                voucher_type: data.header.voucher_type,
                                custom_operational_payment_request: data.header.custom_operational_payment_request,
                                custom_customer_order_reference: data.header.custom_customer_order_reference
                            }, (doc) => {
                                doc.posting_date = data.header.posting_date;
                                doc.user_remark = data.header.user_remark;
                                doc.accounts = [];
                                (data.accounts || []).forEach((source_row) => {
                                    const row = frappe.model.add_child(doc, 'accounts');
                                    Object.assign(row, source_row);
                                });
                            });
                        }
                    });
                }, __('Actions'));
            }
        });
    }
});
