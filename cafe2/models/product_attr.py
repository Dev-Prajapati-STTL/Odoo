from odoo import models, fields

class ProductAttribute(models.Model):
    _name = 'cafe2.product.attribute'
    _description = 'Product Attribute'
    
    name = fields.Char(string='Name', required=True)
