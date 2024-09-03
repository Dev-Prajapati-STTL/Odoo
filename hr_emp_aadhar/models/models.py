# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmpInherited(models.Model):
    _inherit = 'hr.employee'
    _description = 'Inherited Hr Module'

    aadhar_no = fields.Integer('Aadhar')
    

