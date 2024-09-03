#-*- coding:utf-8 -*-

from datetime import datetime
from odoo import api, fields, models, exceptions

class HospitalAppointment(models.Model):
    _name = 'hospital.appointments'
    _description = 'All the appointments'
    _rec_name = "id"

    patient = fields.Many2one('hospital.patient', required=True)
    start_date = fields.Datetime('From', required=True)
    end_date = fields.Datetime('To')

    _sql_constraints = [
        ('start_not_gt_end','check(start_date <= end_date)','Start Date must be before or equal to End Date!')
    ]

    @api.constrains('start_date')
    def start_date_not_past(self):
        for record in self:
            if record.start_date < datetime.now():
                raise exceptions.ValidationError('Past date is not allowed!')
    