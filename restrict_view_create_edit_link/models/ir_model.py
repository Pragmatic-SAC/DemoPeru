# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class IrModel(models.Model):
    _inherit = 'ir.model'

    access_links = fields.One2many(comodel_name='ir.model.access.link', inverse_name='model_id',
                                   string='Access Create Edit Links')

    @api.model
    def check_restricts(self, model_name):
        access_link = self.env['ir.model.access.link'].search(
            [('name', '=', model_name), ('user_id', '=', self.env.user.id)], limit=1)
        if access_link.id:
            return {
                'success': True,
                'hide_create': access_link.hide_create,
                'hide_edit': access_link.hide_edit,
                'hide_unlink': access_link.hide_unlink,
                'hide_duplicate': access_link.hide_duplicate,
                'hide_archived': access_link.hide_archived,
                'hide_create_link': access_link.hide_create_link,
                'hide_edit_link': access_link.hide_edit_link
            }
        else:
            return {'success': False, 'message': _('No restrict for this model.')}


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    access_links = fields.One2many(comodel_name='ir.model.access.link', inverse_name='model_id',
                                   string='Access Create Edit Links')
