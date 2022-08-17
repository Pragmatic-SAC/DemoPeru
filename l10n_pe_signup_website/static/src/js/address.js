$(document).ready(function (event) {
    function AddressForm() {
        var self = this;
        self.typeDocumentWidget;
        self.countryWidget;
        self.districtWidget;
        self.first = true;
        this.init = function () {
            self.loadCountry();
            self.loadDistrict();
            self.loadTypePerson();
            self.loadTypeDocument();
        }
        this.loadTypePerson = function () {
            var type_val = $('input[name ="company_type"]:checked').val();
            if (type_val === undefined) {
                $("#company_type_person").prop("checked", true);
            }
        }
        this.callServiceFetch = function (params, callback) {
            $.ajax({
                method: "GET",
                data: params,
                url: "/pragmatic/signup/selectize",
            }).fail(function (error) {
            }).done(callback);
        }
        this.loadTypeDocument = function () {
            self.callServiceFetch({"type": "type_document"}, function (data) {
                if (data.success) {
                    self.initTypeDocument(data)
                }
            });
        }
        this.initTypeDocument = function (data) {
            self.typeDocumentWidget = $('#l10n_latam_identification_type_id').selectize({
                create: false,
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                options: data.data,
                onChange: function (type_document_id) {
                    var selectize = this;
                    if (type_document_id) {
                        selectize.options[type_document_id]
                        // var type_document = self.typeDocumentWidget[0].selectize.options[type_document_id];
                    }
                },
                onInitialize: function () {
                    var selectize = this;
                    var type_val = $('#selected_l10n_latam_identification_type_id').val();
                    if (type_val) {
                        selectize.addOption(data.data);
                        selectize.setValue(parseInt(type_val));
                    } else {
                        selectize.addOption(data.data);
                        selectize.setValue(data["default"]);
                    }
                }

            });
        }

        this.loadCountry = function () {
            self.callServiceFetch({"type": "country"}, function (data) {
                if (data.success) {
                    self.initCountry(data);
                }
            });
        }
        this.initCountry = function (data) {
            self.countryWidget = $('#pragma_country_id').selectize({
                create: false,
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                options: data.data,
                onChange: function (country_id) {
                    var selectize = this;
                    if (country_id) {
                        selectize.options[country_id]
                        // var country = self.countryWidget[0].selectize.options[country_id];
                        if (self.first === false) {
                            self.changeCountry(country_id)
                        }
                        ;
                    }
                },
                onInitialize: function () {
                    var selectize = this;
                    var type_val = $('#selected_country_id').val();
                    if (type_val) {
                        selectize.addOption(data.data);
                        selectize.setValue(type_val);
                    } else {
                        selectize.addOption(data.data);
                        selectize.setValue(data["default"]);
                    }
                    if (self.first === true) {
                        self.first = false;
                    } else {
                        self.first = true;
                    }
                }
            });
        }

        this.loadDistrict = function () {
            self.callServiceFetch({"type": "district"}, function (data) {
                if (data.success) {
                    self.initDistrict(data)
                }
            });
        }
        this.changeCountry = function (country) {
            self.callServiceFetch({"type": "district", "country": country}, function (data) {
                if (data.success) {
                    $("#l10n_pe_district")[0].selectize.clear(true);
                    $("#l10n_pe_district")[0].selectize.clearOptions();
                    $("#city").val('');
                    $("#zip").val('');
                    $("#l10n_pe_district")[0].selectize.addOption(data.data);
                    // self.initDistrict(data);
                }
            });
        }
        this.initDistrict = function (data) {
            self.districtWidget = $('#l10n_pe_district').selectize({
                create: false,
                persist: false,
                allowEmptyOption: true,
                valueField: 'id',
                labelField: 'name',
                searchField: 'name',
                options: data.data,
                onChange: function (district_id) {
                    var selectize = this;
                    if (district_id) {
                        // var district = self.districtWidget[0].selectize.options[district_id];
                        selectize.options[district_id]
                        var _city = selectize.options[district_id]['city']
                        var _zip = selectize.options[district_id]['zip_code']
                        $("#city").val(_city);
                        $("#zip").val(_zip);
                    }
                },
                onInitialize: function () {
                    var selectize = this;
                    var type_val = $('#selected_l10n_pe_district').val();
                    selectize.options = [];
                    selectize.addOption(data.data);
                    selectize.setValue(type_val);
                },
            });

        }
    }

    var signup = new AddressForm();
    setTimeout(function () {
        signup.init();
    }, 2000);
});

