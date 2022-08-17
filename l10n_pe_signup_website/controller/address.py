# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo.http import request
from odoo import http, _
import werkzeug
import json
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging

_logger = logging.getLogger(__name__)


def get_partner_id():
    user_partner = request.env['res.users'].sudo().browse(request.session.uid)
    return user_partner.partner_id.id or 0


def get_partner_document():
    user_partner = request.env['res.users'].sudo().browse(request.session.uid)
    return user_partner.partner_id.vat or 0


def signup_from_address(newPartner, values):
    if newPartner:
        if len(values['email']) < 2:
            return
        values['login'] = values['email']
        company_id = request.website.company_id.id
        UserCopy = request.env["res.users"].sudo().search(
            [('login', '=', values['login']), ('company_id', '=', company_id)], limit=1)
        if UserCopy.id:
            raise SignupError(_("User exist"))

        new_values = {
            "name": values['name'],
            "login": values["login"],
            "password": values["password"],
        }
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            new_values['lang'] = lang
        new_values["partner_id"] = newPartner
        try:
            db, login, password = request.env['res.users'].sudo().signup(new_values, None)
        except:
            raise SignupError(_("Authentication Failed."))
        request.env.cr.commit()  # as authenticate will use its own cursor we need to commit the current transaction
        uid = request.session.authenticate(db, login, password)
        if not uid:
            raise SignupError(_("Authentication Failed."))


def val_type_document():
    has_document = False
    params = request.params
    company_id = request.website.company_id.id
    if 'l10n_latam_identification_type_id' in params:
        type_doc = params.get('l10n_latam_identification_type_id')
        doc_number = params.get('vat')
        user_partner = request.env['res.partner'].sudo().search(
            [('company_id', '=', company_id), ('l10n_latam_identification_type_id', '=', int(type_doc)),
             ('vat', '=', doc_number)], limit=1)
        if user_partner.id:
            user = request.env['res.users'].sudo().search([('partner_id', '=', user_partner.id)], limit=1)
            if user.id:
                has_document = True
            else:
                has_document = True
    return has_document


class Address(WebsiteSale):
    def _get_mandatory_billing_fields(self):
        response = super(Address, self)._get_mandatory_billing_fields()
        response.append('zip')
        response.append('l10n_pe_district')
        response.remove('city')
        return response

    def _get_mandatory_shipping_fields(self):
        response = super(Address, self)._get_mandatory_shipping_fields()
        response.remove('city')
        return response

    def values_postprocess(self, order, mode, values, errors, error_msg):
        new_values, errors, error_msg = super(Address, self).values_postprocess(
            order, mode, values, errors, error_msg)
        if 'l10n_latam_identification_type_id' in values:
            new_values['l10n_latam_identification_type_id'] = values['l10n_latam_identification_type_id']
        if 'company_type' in values:
            new_values.update({'company_type': values['company_type']})
        if 'phone' in values:
            new_values.update({'phone': values['phone']})
            new_values.update({'mobile': values['phone']})

        if 'l10n_latam_identification_type_id' in values:
            pass
        else:
            errors["l10n_latam_identification_type_id"] = 'error'
            error_msg.append(_('Select the valid document type.'))

        if 'street2' in values:
            new_values.update({'street2': values['street2']})
        if 'l10n_pe_district' in values:
            if type(values['l10n_pe_district']) is int:
                new_values.update({'l10n_pe_district': int(values['l10n_pe_district'])})
                district = request.env["l10n_pe.res.city.district"].sudo().browse(int(values['l10n_pe_district']))
                new_values.update({'state_id': district.city_id.state_id.id, 'city': district.name})
            else:
                errors["l10n_pe_district"] = 'error'
                error_msg.append(_("Select the district from the list correctly."))

        if 'zip' in values:
            new_values.update({'zip': values['zip']})

        if 'email' in values:
            if 'check_bill' not in values:
                if get_partner_id() == 0:
                    UserCopy = request.env["res.users"].sudo().search(
                        [('login', '=', values['email'])], limit=1)
                    if UserCopy.id:
                        errors["user_id"] = 'error'
                        error_msg.append(_('The user already exists, reset password.'))
        if 'type' in values:
            company_id = request.website.company_id.id
            new_values.update({'type': 'contact', 'company_id': company_id})
        if request.website.term_conditions is True and mode[0] != 'edit' and mode[1] != 'shipping':
            if 'shipping_terms' in values:
                new_values.update({'term_conditions': True})
            else:
                errors.update({'shipping_terms': 'error'})
                error_msg.append(_('You must accept the terms and conditions.'))
        if mode[0] == 'edit' and mode[1] == 'billing' and get_partner_document() == 0:
            if 'type' in new_values:
                company_id = request.website.company_id.id
                new_values.update({'type': 'contact', 'company_id': company_id})

        if request.website.term_conditions is True and mode[0] == 'edit' and mode[
            1] != 'shipping' and get_partner_document() == 0:
            if 'shipping_terms' in values:
                new_values.update({'term_conditions': True})
            else:
                errors.update({'shipping_terms': 'error'})
                error_msg.append(_('You must accept the terms and conditions.'))

        return new_values, errors, error_msg

    def values_preprocess(self, order, mode, values):
        if 'name' in values:
            values['name'] = values['name']
        if 'l10n_pe_district' in values and type(values['l10n_pe_district']) is int:
            district = request.env["l10n_pe.res.city.district"].sudo().browse(int(values['l10n_pe_district']))
            values.update({'state_id': district.city_id.state_id.id})
        response = super(Address, self).values_preprocess(order, mode, values)
        return response

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super(Address, self).checkout_form_validate(mode, all_form_values, data)
        if mode[0] == 'new' and mode[1] == 'billing':
            if 'vat' in all_form_values:
                val_doc = val_type_document()
                if val_doc:
                    error["vat"] = 'error'
                    error_message.append(_('The document number is already registered.'))
                else:
                    if 'vat' in error:
                        del error['vat']
                        for index, s in enumerate(error_message):
                            if '10XXXXXXXXY or 20XXXXXXXXY or 15XXXXXXXXY or 16XXXXXXXXY or 17XXXXXXXXY' in s:
                                del error_message[index]
            if 'password' in all_form_values:
                if len(all_form_values['password']) < 8:
                    error["password"] = 'error'
                    error_message.append(_('Passwords must be at least 8 digits long.'))
            if 'vat' in all_form_values and 'l10n_latam_identification_type_id' in all_form_values:
                env_indentify = request.env['l10n_latam.identification.type'].sudo().browse(
                    int(all_form_values['l10n_latam_identification_type_id']))
                if env_indentify.placeholder is False:
                    error["vat"] = 'error'
                    error_message.append(_(
                        'Validation digits for the document type are missing, contact the administrator.'))
                else:
                    len_doc = len(env_indentify.placeholder)
                    if len_doc != len(all_form_values['vat']):
                        error["vat"] = 'error'
                        error_message.append(
                            _('Invalid document number, verify number of digits according to document type.'))
        elif mode[0] == 'edit' and mode[1] == 'billing' and get_partner_document() == 0:
            if 'vat' in all_form_values and 'l10n_latam_identification_type_id' in all_form_values:
                env_indentify = request.env['l10n_latam.identification.type'].sudo().browse(
                    int(all_form_values['l10n_latam_identification_type_id']))
                if 'vat' in all_form_values:
                    val_doc = val_type_document()
                    if val_doc:
                        error["vat"] = 'error'
                        error_message.append(_('The document number is already registered.'))
                    else:
                        if 'vat' in error:
                            del error['vat']
                if env_indentify.placeholder is False:
                    error["vat"] = 'error'
                    error_message.append(_(
                        'Validation digits for the document type are missing, contact the administrator.'))
                else:
                    len_doc = len(env_indentify.placeholder)
                    if len_doc != len(all_form_values['vat']):
                        error["vat"] = 'error'
                        error_message.append(
                            _('Invalid document number, verify number of digits according to document type.'))

        else:
            if 'vat' in error:
                del error['vat']

        return error, error_message

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        response = super(Address, self).address(**kw)
        response.qcontext['logged'] = get_partner_id()
        response.qcontext['document'] = get_partner_document()
        response.qcontext['has_terms'] = request.website.term_conditions
        response.qcontext['terms_link'] = request.website.link_term_conditions
        # if not request.session.uid:
        #     order = request.website.sale_get_order()
        #     if 'submitted' in request.params:
        #         if order.partner_id.id:
        #             _context = response.qcontext
        #             if "error" in _context:
        #                 haveError = False
        #                 for key, value in _context.items():
        #                     haveError = True
        #                 if haveError:
        #                     return response
        #                 if 'password' in _context["error"]:
        #                     return response
        #                 if 'email' in _context["error"]:
        #                     return response
        #             signup_from_address(order.partner_id.id, kw)
        if 'partner_id' in response.qcontext:
            if response.qcontext['partner_id'] > 0:
                partner_id = response.qcontext['partner_id']
                partner = request.env['res.partner'].sudo().browse(partner_id)
                values = {
                    'company_type': partner.company_type,
                    'name': partner.name or '',
                    'l10n_latam_identification_type_id': partner.l10n_latam_identification_type_id.id or
                                                         response.qcontext['checkout'][
                                                             'l10n_latam_identification_type_id'] if 'l10n_latam_identification_type_id' in
                                                                                                     response.qcontext[
                                                                                                         'checkout'] else '',
                    'email': partner.email or ''
                }
                if response.qcontext['checkout'].get('phone', False):
                    values['phone'] = partner.phone or response.qcontext['checkout']['phone']
                if response.qcontext['checkout'].get('vat', False):
                    values['vat'] = partner.vat or response.qcontext['checkout']['vat']
                if response.qcontext['checkout'].get('street', False):
                    values['street'] = partner.street or response.qcontext['checkout']['street']
                if response.qcontext['checkout'].get('street2', False):
                    values['street2'] = partner.street2 or response.qcontext['checkout']['street2']
                if response.qcontext['checkout'].get('country_id', False):
                    values['country_id'] = partner.street2 or response.qcontext['checkout']['country_id']
                if response.qcontext['checkout'].get('l10n_pe_district', False):
                    values['l10n_pe_district'] = partner.street2 or response.qcontext['checkout']['l10n_pe_district']
                response.qcontext['checkout'] = values
        return response


def response_json(obj_json):
    return werkzeug.wrappers.Response(
        status=200,
        content_type="application/json; charset=utf-8",
        headers=[("Cache-Control", "no-store"), ("Pragma", "no-cache")],
        response=json.dumps(obj_json),
    )


class LocalizationSignUp(http.Controller):
    @http.route('/pragmatic/signup/selectize', type='http', auth='none', methods=['GET'], csrf=False, website=True)
    def signup_selectize(self, type, country=None):
        if type == "country":
            return response_json(self.get_countries())
        if type == "district":
            return response_json(self.get_districts(country))
        if type == "type_document":
            return response_json(self.get_type_documents())

    def get_countries(self):
        env_country = request.env["res.country"].sudo()
        current_website = request.env['website'].sudo().get_current_website()
        default_country = current_website.company_id.country_id.id
        user_partner = request.env['res.users'].sudo().browse(request.session.uid)
        partner = user_partner.partner_id or 0
        kws = {
            "domain": [('code', '!=', False)],
            "fields": ['id', 'code', 'name', 'phone_code']
        }
        countries = env_country.with_context(lang=request.context.get('lang', False)).search_read(**kws)
        if partner != 0 and get_partner_document() != 0:
            default_country = partner.country_id.id
        return {"success": True, "data": countries, "default": default_country}

    def get_districts(self, country):
        env_district = request.env["l10n_pe.res.city.district"].sudo()
        current_website = request.env['website'].sudo().get_current_website()
        default_country = country or current_website.company_id.country_id.id
        districts = []
        for dis in env_district.with_context(lang=request.context.get('lang', False)).search(
                [('code', '!=', False), ('city_id.state_id.country_id.id', '=', default_country)]):
            districts.append({
                "id": dis.id,
                "name": "%s - %s - %s" % (dis.name, dis.city_id.name, dis.city_id.state_id.name),
                "city": dis.name,
                "zip_code": dis.code

            })
        user_partner = request.env['res.users'].sudo().browse(request.session.uid)
        partner = user_partner.partner_id or 0
        default_district = 0
        if partner != 0 and get_partner_document() != 0:
            default_country = partner.country_id.id
            default_district = partner.l10n_pe_district.id
        return {"success": True, "data": districts, "default": default_country, 'default_district': default_district}

    def get_type_documents(self):
        env_type_document = request.env["l10n_latam.identification.type"].sudo()
        type_default = env_type_document.search([('active', '=', True), ('l10n_pe_vat_code', '=', 1)],
                                                limit=1)
        documents = []
        for item in env_type_document.with_context(lang=request.context.get('lang', False)).search(
                [('active', '=', True)]):
            documents.append({
                "id": item.id,
                "name": item.name,
                "minimal_length": int(item.placeholder) or 0,
            })
        user_partner = request.env['res.users'].sudo().browse(request.session.uid)
        partner = user_partner.partner_id or 0
        if partner != 0 and get_partner_document() != 0:
            type_default = partner.l10n_latam_identification_type_id

        return {"success": True, "data": documents, "default": type_default.id}
