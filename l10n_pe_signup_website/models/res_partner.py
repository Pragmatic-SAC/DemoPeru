# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    term_conditions = fields.Boolean(string="Has Terms and Conditions", default=False)
