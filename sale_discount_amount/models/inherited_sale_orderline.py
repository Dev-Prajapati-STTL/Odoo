from odoo import fields,exceptions,api,models

class sale_orderline_inherited(models.Model):
    _inherit = 'sale.order.line'
    _description = 'Inherited Sale Order Line'
    
    discount_percent = fields.Float('Discount')