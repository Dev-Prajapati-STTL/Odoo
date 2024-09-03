from odoo import api, fields, models, exceptions

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread']
    _description = "Patient's Records"

    sequence_no = fields.Char('Sequence Number', default=lambda self: self._assign_seq_no(), readonly=True)
    name = fields.Char(string="Patient Name", required=True, tracking=True)
    age = fields.Integer(string="Age")
    is_child = fields.Boolean(string="Is Child?", compute='_is_child')
    eligible_for_voting = fields.Boolean(string="Is Eligible for Voting?", readonly=True)
    years_until_retirement = fields.Integer(string="Years until Retirement", readonly=True)
    notes = fields.Text(string="Notes")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], string="Gender")
    code_name_age_gender = fields.Char(string="Unique Code", readonly=True)

    def _assign_seq_no(self):
        return self.env['ir.sequence'].next_by_code('hospital.sequence.number') 

    # @api.model
    # def default_get(self,fields_list):
    #     res = super(HospitalPatient, self).default_get(fields_list)
    #     if not res.get('sequence_no'):
    #         res['sequence_no'] = self.env['ir.sequence'].next_by_code('hospital.sequence.number')
    #     return res

    # @api.model
    # def create(self, vals):
    #     print(vals)
    #     vals['sequence_no'] = self.env['ir.sequence'].next_by_code('hospital.sequence.number')
    #     return super(HospitalPatient, self).create(vals)
    
    @api.onchange('age')
    def is_18_above(self):
        for record in self:
            record.eligible_for_voting = record.age > 18
            if record.age >= 65:
                record.years_until_retirement = 0
            else:
                record.years_until_retirement = 65 - record.age

    @api.depends('age')
    def _is_child(self):
        for record in self:
            record.is_child = record.age < 18

    @api.onchange("sequence_no","name","age","gender")
    def make_combo(self):
        for record in self:
            record.code_name_age_gender = f'{record.sequence_no}-{record.name}-{record.age}-{record.gender}'
    
    @api.onchange('notes')
    def _err_if_no_value(self):
        for record in self:
            if record.notes and not record.name:
                raise exceptions.UserError("name cannot be empty!")
    

