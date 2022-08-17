from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _create_invoice(self, order, so_line, amount):
        invoice = super(SaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        invoice._pg_onchange_partner()
        return invoice

    def _prepare_invoice_values(self, order, name, amount, so_line):
        response = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        for index in range(0, len(response.get('invoice_line_ids', []))):
            response['invoice_line_ids'][index][2]['price_ref'] = so_line.price_unit
        invoice_type_allowed = order.partner_id.l10n_latam_identification_type_id.invoice_type_allowed
        if invoice_type_allowed.ids:
            response['l10n_latam_document_type_id'] = invoice_type_allowed.ids[0]
        return response
