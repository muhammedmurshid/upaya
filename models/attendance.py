from odoo import models, fields, api


class BatchStudentsAttendance(models.Model):
    _name = 'upaya.students.attendance'

    name = fields.Char('Name')
    attendance = fields.Selection([('full_day', 'Full Day'), ('half_day', 'Half Day'), ('absent', 'Absent')], string='Attendance')
    student_id = fields.Integer()
    upaya_id = fields.Many2one('upaya.form', string="Upaya")
