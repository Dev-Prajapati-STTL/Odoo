from odoo import api, fields, models, exceptions


class Tags(models.Model):
    _name = 'cafe.tagz'
    _description = 'All the tags'
    _rec_name = 'tag_name'

    tag_name = fields.Char(string='Tag Name', required=True)
    tag_color = fields.Integer(string='Tag Color')

    # def name_get(self):
    #     res = []
    #     for record in self:
    #         name = f'{record.tag_name} - {record.tag_color}'
    #         res.append((record.id, name))
    #     return res

    @api.onchange('tag_name')
    def prnt_cafe_tags(self):
        print("In cafe's print methoddd\n\n\n")

