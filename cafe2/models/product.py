from odoo import api, fields, models, exceptions
import logging

_logger = logging.getLogger(__name__)

class CafeProducts(models.Model):
    _name = 'cafe.products'
    _inherit = 'cafe.products'
    _description = 'All the Cafe Products'

    product_attrs_id = fields.One2many('cafe2.product.attributes','product_id',string='Product Attributes')
    product_type = fields.Selection([('consumable','Consumable'),('stockable','Stockable'),('service','Service')])

    def cafe2_action_create_variants(self):
        _logger.info("Executing cafe2_action_crezate_variants")
        for product in self:
            _logger.info(f"First loop - {type(product.product_attrs_id)}")
            for value in product.product_attrs_id:
                _logger.info(f"Creating variant for attribute value: {value}")
                self.env['cafe2.product.variant'].create({
                    'products_id': product.id,
                    'attribute_value_ids': [(6, 0, [val.id for val in value.attribute_value_ids])], 
                })
        _logger.info("Finished creating variants")
    
    @api.constrains('product_code')
    def _code_not_gt_4(self):
        for record in self:
            if len(record.product_code) != 2:
                raise exceptions.ValidationError('Product Code must exactly of length 2')

    
    