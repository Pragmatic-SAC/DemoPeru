# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class IrModelAccessLink(models.Model):
    _name = 'ir.model.access.link'
    _description = 'Model allows to show or hide link create and edit.'

    name = fields.Char(string='Model Name', compute='_compute_name', store=True)

    @api.depends('model_id')
    def _compute_name(self):
        for model in self:
            model.name = model.model_id.model

    model_id = fields.Many2one(comodel_name='ir.model', string='Model', ondelete='cascade')
    user_id = fields.Many2one(comodel_name='res.users', string='User', required=True)

    hide_create = fields.Boolean(string='Hide Create Button')
    hide_edit = fields.Boolean(string='Hide Edit Button')
    hide_unlink = fields.Boolean(string='Hide Delete Action')
    hide_duplicate = fields.Boolean(string='Hide Duplicate Action')
    hide_archived = fields.Boolean(string='Hide Button Archived')
    hide_create_link = fields.Boolean(string='Hide Create Link')
    hide_edit_link = fields.Boolean(string='Hide Edit Link')

    _sql_constraints = [
        ('model_user_unique', 'unique (user_id, model_id)',
         'You cannot have two records for the same user.')
    ]
