from odoo import api,fields,models

class Cafe2Tags(models.Model):
    _name = 'cafe.tagz'
    _inherit = 'cafe.tagz'
    _description = 'All the tags of cafe2'

    cost_price = fields.Integer("Cost Price")
    sale_price = fields.Integer("Sale Price")
    gpm = fields.Integer("GPM",compute='compute_gpm')
    taxes = fields.Many2many('cafe.taxes')
    note = fields.Text('Note')

    @api.depends('cost_price','sale_price')
    def compute_gpm(self):
        for record in self:
            record.gpm = record.sale_price - record.cost_price
    
    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == 'tree':
            note = arch.xpath("//field[@name='note']")[0]
            note.set("string", "Notes")
        return arch, view
    
    @api.onchange('cost_price')
    def prnt_cafe_tags(self):
        super().prnt_cafe_tags()
        self.note = 'Cost Price changed!'
