# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    can_edit_price = fields.Boolean(compute='_compute_can_edit')
    can_edit_cost = fields.Boolean(compute='_compute_can_edit')

    @api.depends("type")
    def _compute_can_edit(self):
        for product in self:
            product.can_edit_price = self.sudo().env.user.has_group('pg_product_security.security_product_price')
            product.can_edit_cost = self.sudo().env.user.has_group('pg_product_security.security_product_cost')
