from lxml import etree
from odoo import api, fields, models, exceptions

class Product(models.Model):
    _name = 'cafe.products'
    _description = 'All the products'
    _rec_name = 'product_name'

    product_name = fields.Char(string='Product Name', required=True)
    product_code = fields.Char(string='Product Code', required=True)
    product_image = fields.Image(string='Product Image')
    cost_price = fields.Float(string='Cost Price', required=True, default=0.0)
    sale_price = fields.Float(string='Sale Price', required=True, default=0.0)
    gpm = fields.Float(string='GPM', compute='_compute_gpm', store=True)
    tags = fields.Many2many('cafe.tagz')

    _sql_constraints = [
        ('product_code_uniq', 'UNIQUE(product_code)', 'The product code must be unique!'),
        ('product_name_code_uniq', 'UNIQUE(product_name, product_code)', 'The combination of product name and code must be unique!'),
        ('product_price_gt_zero', 'CHECK(cost_price > 0.0 AND sale_price > 0.0 AND cost_price <= sale_price)',
         'The product price must be valid!'),
        ('product_gpm_lt_200', 'CHECK(gpm < 200)','The product gpm must be under 200!'),
    ]

    def action_print_report(self):
        return self.env.ref('cafe.cafe_products_action_report').report_action(self)

    @api.constrains('product_code')
    def _code_not_gt_4(self):
        for record in self:
            if len(record.product_code) != 4:
                raise exceptions.ValidationError('Product Code must exactly of length 4')

    @api.depends('cost_price', 'sale_price')
    def _compute_gpm(self):
        for record in self:
            record.gpm = record.sale_price - record.cost_price

    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.product_name} - {record.product_code}"
            result.append((record.id, name))
        return result

    def _name_search(self, name='', args=None, operator='ilike', limit=10):
        if args is None:
            args = []
        if name:
            args += ['|', ('product_name', operator, name), ('product_code', operator, name)]
        return super(Product, self)._name_search(name, args, operator, limit)

    @api.model
    def name_create(self, name):
        record = self.create({'product_name': name, 'product_code': name[:4].upper()})
        return record.id, record.product_name

    def unlink(self):
        for product in self:
            if self.env['cafe.order.line'].search_count([('product_id', '=', product.id)]) > 0:
                raise exceptions.UserError('You cannot delete a product that is referenced in order lines.')
        return super(Product, self).unlink()
    
    @api.onchange('gpm')
    def _domain_on_related_fields(self):
        if self.gpm:
            if self.gpm < 100:
                return {
                        'domain': {
                        'tags': [('tag_name', 'in', ['Green', 'Blue'])]
                    }
                }
            else:
                return {
                    'domain': {
                        'tags': []
                    }
                }
        else:
            return {
                'domain': {
                    'tags': []
                }
            }
    
    @api.model
    def _get_view(self, view_id=None, view_type=None, **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == 'tree':
            gpm_ref = arch.xpath("//field[@name='gpm']")
            if gpm_ref:
                gpm_ref[0].set("string", "GPM")
        
        # if view_type == 'form':
        #     sale_price_ref = arch.xpath("//field[@name='sale_price']")
        #     if sale_price_ref:
        #         sale_price_ref[0].set("readonly", "1")
                
        return arch, view
    


    
    
