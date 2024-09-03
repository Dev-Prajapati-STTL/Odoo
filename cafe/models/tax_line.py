from odoo import api, fields, models


class TaxLine(models.Model):
    _name = 'cafe.tax.line'
    _description = 'All the taxlines'
    _rec_name = 'id'

    sale_id = fields.Many2one('cafe.sales', string='Sales Order', ondelete='cascade')
    tax_id = fields.Many2one('cafe.taxes', string='Tax', required=True)
    base_price = fields.Float(string='Base Price', compute='_base_price')
    percentage = fields.Float(string='Percentage', related='tax_id.tax_percent')
    tax_amount = fields.Float(string='Tax Amount', compute='_tax_amount')

    @api.depends('sale_id.order_line_ids.sub_total', 'tax_id')
    def _base_price(self):
        for line in self:
            base_price = sum(
                order_line.sub_total for order_line in line.sale_id.order_line_ids if line.tax_id in order_line.taxes)
            line.base_price = base_price

    @api.depends('base_price', 'percentage')
    def _tax_amount(self):
        for line in self:
            line.tax_amount = line.base_price * (line.percentage / 100)
