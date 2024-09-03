from odoo import models, fields, api

class ProductAttributes(models.Model):
    _name = 'cafe2.product.attributes'
    _description = 'Product Attributes'
    _rec_name = 'attribute_id'
    
    product_id = fields.Many2one('cafe.products')
    attribute_id = fields.Many2one('cafe2.product.attribute', string='Attribute')
    attribute_value_ids = fields.Many2many('cafe2.product.attribute.value', string='Attribute Values')
