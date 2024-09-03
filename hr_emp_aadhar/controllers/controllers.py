# -*- coding: utf-8 -*-
# from odoo import http


# class HrEmpAadhar(http.Controller):
#     @http.route('/hr_emp_aadhar/hr_emp_aadhar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_emp_aadhar/hr_emp_aadhar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_emp_aadhar.listing', {
#             'root': '/hr_emp_aadhar/hr_emp_aadhar',
#             'objects': http.request.env['hr_emp_aadhar.hr_emp_aadhar'].search([]),
#         })

#     @http.route('/hr_emp_aadhar/hr_emp_aadhar/objects/<model("hr_emp_aadhar.hr_emp_aadhar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_emp_aadhar.object', {
#             'object': obj
#         })
