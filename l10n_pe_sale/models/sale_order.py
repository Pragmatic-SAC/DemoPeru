from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        response = super()._prepare_invoice()
        invoice_type_allowed = self.partner_id.l10n_latam_identification_type_id.invoice_type_allowed
        if invoice_type_allowed.ids:
            response['l10n_latam_document_type_id'] = invoice_type_allowed.ids[0]
            series = self.env["pragmatic.serie.sequence"] \
                .get_sequence_by_user_establishment_vals(response['user_id'],
                                                         False,
                                                         response['l10n_latam_document_type_id'],
                                                         response['company_id'],
                                                         response['journal_id'])
            if series.ids:
                response['establishment'] = series[0].establishment.id
                response['serie_id'] = series[0].id
                response['serie_code'] = series[0].sequence_id.prefix
        return response
