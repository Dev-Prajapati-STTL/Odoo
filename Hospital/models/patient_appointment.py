from odoo import api, fields, models, exceptions

class HospitalCombine(models.Model):
    _name = 'hospital.combine'
    _inherit = ['hospital.patient','hospital.appointments']
    _description = 'All the combinations'

    date = fields.Date(default=fields.Date.context_today, readonly='1')



    