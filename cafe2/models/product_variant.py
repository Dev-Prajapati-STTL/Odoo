from odoo import models, fields, api

class ProductVariant(models.Model):
    _name = 'cafe2.product.variant'
    _inherits = {'cafe.products':'products_id'}
    _description = 'All the product variants'
    
    products_id = fields.Many2one('cafe.products')
    attribute_value_ids = fields.Many2many('cafe2.product.attribute.value', string='Attribute Values')
    price = fields.Float(string='Price', compute='_compute_price', store=True)

    @api.depends('attribute_value_ids')
    def _compute_price(self):
        for variant in self:
            base_price = variant.products_id.sale_price
            attribute_price = sum(value.cost for value in variant.attribute_value_ids)
            variant.price = base_price + attribute_price

    def name_get(self):
        variants = []
        for record in self:
            attribute_names = ', '.join(record.attribute_value_ids.mapped('name'))
            name = f'{record.products_id.product_name} - {attribute_names}'
            variants.append((record.id, name))
        return variants
