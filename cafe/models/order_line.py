from odoo import api, fields, models


class OrderLine(models.Model):
    _name = 'cafe.order.line'
    _description = 'All the orderlines'
    _rec_name = 'sale_id'

    product_id = fields.Many2one('cafe.products', string="Products", ondelete='restrict')
    sale_id = fields.Many2one('cafe.sales', string='Sale ID', ondelete='cascade')
    quantity = fields.Float(string="Quantity")
    price = fields.Float(string="Unit Price", related='product_id.sale_price', readonly='1')
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

    @api.onchange('sub_total')
    def _domain_on_related_fields(self):
        if self.sub_total < 1000.00:
            return {
                'domain':{
                    'taxes': [('tax_name','in',['CGST','SGST'])]
                }
            }
        else:
            return {
                'domain':{
                    'taxes': []
                }
            }
