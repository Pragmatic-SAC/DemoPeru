# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class PGRestrict(http.Controller):

    @http.route(['/pg_restrict'], type='json', auth='user')
    def pg_restrict(self, **kw):
        IrModelEnv = request.env['ir.model']
        vals = IrModelEnv.check_restricts(kw.get('model_name'))
        return vals
