# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class Website(models.Model):
    _inherit = "website"

    term_conditions = fields.Boolean(string="Has Terms and Conditions")
    link_term_conditions = fields.Char(string="URL Terms and Conditions")
