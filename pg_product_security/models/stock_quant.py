# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class ProductTemplate(models.Model):
    _inherit = "stock.quant"

    can_edit_quantity = fields.Boolean(compute='_compute_can_edit')

    def _compute_can_edit(self):
        for product in self:
            product.can_edit_quantity = self.sudo().env.user.has_group('pg_product_security.security_product_quantity')
