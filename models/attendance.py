from odoo import models, fields, api


class BatchStudentsAttendance(models.Model):
    _name = 'upaya.students.attendance'

    name = fields.Char('Name', required=True)
    attendance = fields.Boolean(string="Attendance", default='present')
    student_id = fields.Integer()
    upaya_id = fields.Many2one('upaya.form', string="Upaya")