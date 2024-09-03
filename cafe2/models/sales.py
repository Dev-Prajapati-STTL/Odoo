from odoo import api, fields, models

class InheritedCafeSales(models.Model):
    _name = 'cafe.sales'
    _inherit = ['cafe.sales','mail.thread']
    # _inherits = {'cafe.sales':'cafe2_sales_rel_id'}
    _description = 'All the inherited cafe sales'

    # cafe2_sales_rel_id = fields.Many2one('cafe.sales')
    customer_id = fields.Many2one(tracking=True)
    date = fields.Date(tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('rvrt', 'Reverted'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('canceled', 'Canceled')
    ], string='State', default='draft', tracking=True)
    order_number = fields.Char(tracking=True)
    order_line_ids = fields.One2many(tracking=True)
    # order_line_ids = fields.One2many('cafe2.order.line','sales_id',tracking=True)
    tax_line_ids = fields.One2many(tracking=True)
    untaxed_amount = fields.Float(tracking=True)
    tax_amount = fields.Float(tracking=True)
    total_amount = fields.Float(tracking=True)

    def action_confirm(self):
        if self.order_number == 'New':
            self.order_number = self.env['ir.sequence'].next_by_code('cafe.sale.order')
        self.write({'state': 'confirmed'})
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Sale order is confirmed',
                'type': 'rainbow_man',
            } 
        }
    
    def rvrt_to_draft(self):
        self.update({'state': 'rvrt'})
        return True
