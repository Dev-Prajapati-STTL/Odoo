from odoo import api, fields, models, exceptions


class Sales(models.Model):
    _name = 'cafe.sales'
    _description = 'All the sales'
    _rec_name = 'id'
    _order = 'date desc'

    customer_id = fields.Many2one('res.partner', string='Responsible',required=True)
    customer_name = fields.Char(related='customer_id.name', store=True)
    date = fields.Date(string='Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('canceled', 'Canceled')
    ], string='State', default='draft')
    order_number = fields.Char(string='Order Reference', default="New", readonly=True, copy=False)
    order_line_ids = fields.One2many('cafe.order.line', 'sale_id', string='Order Lines', ondelete='restrict')
    tax_line_ids = fields.One2many('cafe.tax.line', 'sale_id', string='Tax Lines', store=True, compute='_compute_tax_line_ids')
    untaxed_amount = fields.Float(string='Untaxed Amount', store=True, compute='_compute_untaxed_amount')
    tax_amount = fields.Float(string='Tax Amount', store=True, compute='_compute_tax_amount')
    total_amount = fields.Float(string='Total Amount', store=True, compute='_compute_total')
    color = fields.Integer("Color")

    @api.model
    def default_get(self, fields_list):
        res = super(Sales, self).default_get(fields_list)

        res.update({    
            'date': fields.Date.context_today(self)
        })

        return res

    @api.depends('order_line_ids.sub_total')
    def _compute_untaxed_amount(self):
        for record in self:
            record.untaxed_amount = sum(line.sub_total for line in record.order_line_ids)

    @api.depends('order_line_ids.sub_total')
    def _compute_tax_amount(self):
        for record in self:
            record.tax_amount = sum(orderline.tax_amount for orderline in record.order_line_ids)

    @api.depends('untaxed_amount', 'tax_amount')
    def _compute_total(self):
        for record in self:
            record.total_amount = record.untaxed_amount + record.tax_amount

    @api.depends('order_line_ids')
    def _compute_tax_line_ids(self):
        for record in self:
            record.tax_line_ids = [(5, 0, 0)]
            tax_lines = []
            for line in record.order_line_ids:
                for tax in line.taxes:
                    existing_tax_line = next((tl for tl in self.tax_line_ids if tl.tax_id == tax), None)
                    if existing_tax_line:
                        existing_tax_line.base_price += line.sub_total
                    else:
                        tax_lines.append({
                            'tax_id': tax.id,
                            'base_price': line.sub_total,
                        })

            if tax_lines:
                record.tax_line_ids = [(0, 0, tl) for tl in tax_lines]
            else:
                record.tax_line_ids = []

    def action_confirm(self):
        for record in self:
            record.order_number = self.env['ir.sequence'].next_by_code('cafe.sale.order')
        self.update({'state': 'confirmed'})
        return True

    def action_done(self):
        self.update({'state': 'done'})
        return True

    def action_cancel(self):
        self.update({'state': 'canceled'})
        return True

    def action_draft(self):
        self.update({'state': 'draft'})
        return True

    @api.constrains('date')
    def order_date_not_past(self):
        for record in self:
            if record.date < fields.Date.context_today(self):
                raise exceptions.ValidationError('Past date is not allowed!')
    
