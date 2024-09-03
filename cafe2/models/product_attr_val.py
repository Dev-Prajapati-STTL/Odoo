from odoo import api, fields, models

class ProductAttributeValue(models.Model):
    _name = 'cafe2.product.attribute.value'
    _description = 'Product Attribute Value'
    
    name = fields.Char(string='Name', required=True)
    cost = fields.Float(string='Cost')
    attribute_id = fields.Many2one('cafe2.product.attribute', string='Attribute')
