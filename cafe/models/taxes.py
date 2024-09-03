from odoo import api, fields, models


class Taxes(models.Model):
    _name = 'cafe.taxes'
    _description = 'All the taxes'
    _rec_name = 'tax_name'

    tax_name = fields.Char(string='Tax name', required=True)
    tax_code = fields.Char(string='Tax code', required=True)
    tax_percent = fields.Float(string='Tax percent', required=True)