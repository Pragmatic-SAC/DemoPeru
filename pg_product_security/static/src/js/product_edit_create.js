odoo.define('it_product_security.product_no_create_edit', function (require) {
    "use strict";
    /*
    Create or Edit Product in field many2one, depend for rol create edit
     */
    var session = require('web.session');
    var relational_fields = require('web.relational_fields');
    initWidgetCreateEdit();

    function initWidgetCreateEdit() {
        var ProductFieldNoCreateEdit = relational_fields.FieldMany2One.include({
            _render: function () {
                var self = this;
                if (self.field.relation == "product.product" || self.field.relation == "product.template") {
                    session.user_has_group('pg_product_security.security_product_no_create_edit_views').then(function (has_restriction) {
                        var has_create = true;
                        if (has_restriction) {
                            has_create = false;
                        }
                        self.attrs.options.quick_create = has_create;
                        self.attrs.options.no_create = has_restriction;
                        self.attrs.options.no_create_edit = has_restriction;
                        self.attrs.options.no_open = has_restriction;
                        self.can_create = has_create;
                        self.can_write = has_create;
                    });
                }
                self._super.apply(self, arguments);
            }
        });
    }
});