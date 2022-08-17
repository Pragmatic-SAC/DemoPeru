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
odoo.define('restrict_view_create_edit_link.BasicView', function (require) {
    'use strict';

    var session = require('web.session');
    var BasicView = require('web.BasicView');

    BasicView.include({
        init: function (viewInfo, params) {
            var self = this;
            this._super.apply(this, arguments);
            session.rpc('/pg_restrict', {'model_name': self.controllerParams.modelName}).then(function (vals) {
                console.log("vals", vals);
                if (vals.success) {
                    if (vals.hide_create) {
                        self.controllerParams.activeActions.create = false;
                    }
                    if (vals.hide_edit) {
                        self.controllerParams.activeActions.edit = false;
                    }
                    if (vals.hide_unlink) {
                        self.controllerParams.activeActions.delete = false;
                    }
                    if (vals.hide_duplicate) {
                        self.controllerParams.activeActions.duplicate = false;
                    }
                    if (vals.hide_archived) {
                        self.controllerParams.archiveEnabled = false;
                    }
                } else {
                    console.log('Get Restrict', vals.message);
                }
            }).guardedCatch(function (error) {
                console.error('Get Restrict Error: ', error);
            });
        },
    });
});