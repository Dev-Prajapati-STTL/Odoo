from odoo import api,fields,models

class Cafe2OrderLines(models.Model):
    _name = 'cafe2.order.line'
    _inherits = {'cafe.order.line': 'orderline_rel_id'}
    _description = 'All the inherited taxlines'

    orderline_rel_id = fields.Many2one('cafe.order.line')
    sales_id = fields.Many2one('cafe.sales')
    product_id = fields.Many2one('cafe2.product.variant')
    price = fields.Float(string="Unit Price", related='product_id.price', readonly=True)
    sub_total = fields.Float(string="Sub-Total", compute='_compute_sub_total', store=True)
    taxes = fields.Many2many('cafe.taxes', string='Taxes')
    tax_amount = fields.Float(string='Tax Amount', compute='_compute_tax_amount', store=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('quantity', 'price')
    def _compute_sub_total(self):
        for line in self:
            line.sub_total = line.quantity * line.price

    @api.depends('taxes', 'sub_total')
    def _compute_tax_amount(self):
        for line in self:
            line.tax_amount = sum(tax.tax_percent * line.sub_total / 100 for tax in line.taxes)

    @api.depends('sub_total', 'tax_amount')
    def _compute_total(self):
        for line in self:
            line.total = line.sub_total + line.tax_amount
    