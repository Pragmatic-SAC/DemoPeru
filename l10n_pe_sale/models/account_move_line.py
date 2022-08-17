from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    price_ref = fields.Float(string='Unit Price', digits='Product Price')
