odoo.define('it_lztn_pe_product_stock.BasicView', function (require) {
    "use strict";

    var session = require('web.session');
    var BasicView = require('web.BasicView');
    BasicView.include({
        init: function (viewInfo, params) {
            var self = this;
            this._super.apply(this, arguments);
            var model = self.controllerParams.modelName in ['product.product', 'product.template'] ? 'True' : 'False';
            if (model) {
                session.user_has_group('pg_product_security.security_product_archive').then(function (has_group) {
                    if (!has_group) {
                        self.controllerParams.archiveEnabled = 'False' in viewInfo.fields;
                    }
                });
            }
        },
    });
});