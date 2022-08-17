/**********************************************************************************
 *
 *    Copyright (c) 2020-today Pragmatic S.A.C.
 *
 *    This file is part of Restrict View Create/Link
 *    (see https://mukit.at).
 *
 *    Odoo License v1.0
 *
 **********************************************************************************/
odoo.define('restrict_view_create_edit_link.model_no_create_edit_link', function (require) {
    "use strict";

    var session = require('web.session');
    var RelationalFields = require('web.relational_fields');

    RelationalFields.FieldMany2One.include({
        _render: function () {
            var self = this;

            session.rpc('/pg_restrict', {'model_name': self.field.relation}).then(function (vals) {
                if (vals.success) {
                    if (vals.hide_create_link) {
                        self.can_create = false;
                    }
                    if (vals.hide_edit_link) {
                        self.attrs.options.no_open = true;
                        self.attrs.options.quick_create = false;
                        self.attrs.options.no_create = true;
                        self.attrs.options.no_create_edit = true;
                    }
                } else {
                    console.log('Get Restrict', vals.message);
                }
            }).guardedCatch(function (error) {
                console.error('Get Restrict Error: ', error);
            });
            self._super.apply(self, arguments);
        }
    });
});