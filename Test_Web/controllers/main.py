# -*- coding : utf-8 -*-
from odoo import http, models, fields, _
from odoo.exceptions import AccessError
from odoo.http import request, SessionExpiredException

class MainController(http.Controller):

    @http.route('/create/sale', type='http', auth='public', website=True)
    def create_product(self):
        print(f"\n\n\n\n ID of current user: {request.session.uid } \n\n\n\n\n")
        return request.render('Test_Web.custom_website_create_product')
    
    @http.route('/done_product', type='http', auth='public', website=True)
    def record_created(self, **kwargs):
        print(kwargs)
        request.env['cafe.products'].sudo().create({**kwargs,'product_code': kwargs['product_name'][:2].upper()})
        return request.render('Test_Web.product_thank_you', {'name': kwargs['product_name']})
    
    @http.route('/gen_ticket', type='http', auth='public', website=True)
    def generate_ticket(self):
        return request.render('Test_Web.custom_website_create_ticket')
    
    @http.route('/done_ticket', type='http', auth='public', website=True)
    def record_created(self, **kwargs):
        print(kwargs)
        # request.env['cafe.products'].sudo().create({**kwargs,'product_code': kwargs['product_name'][:2].upper()})
        return request.render('Test_Web.ticket_thank_you')
    
    @http.route('/create/user', type='http', auth='public', website=True)
    def create_user(self):
        return request.render('Test_Web.custom_website_create_user')
