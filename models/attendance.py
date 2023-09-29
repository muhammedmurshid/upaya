from odoo import models, fields, api


class BatchStudentsAttendance(models.Model):
    _name = 'upaya.students.attendance'

    name = fields.Char('Name')
    student_id = fields.Integer()
    upaya_id = fields.Many2one('upaya.form', string="Upaya")
    team_id = fields.Many2one('upaya.teams', string="Team")
    attendance = fields.Boolean('Attendance', default=True)
    topic_for_presentation = fields.Char('Topic For Presentation', related='team_id.topic_for_presentation')

    @api.depends('upaya_id.state')
    def _compute_onchange_state(self):
        print('fksfghsd')
        for i in self:
            if self.upaya_id.state == 'confirm':
                i.state = 'confirm'
            if self.upaya_id.state == 'training_completed':
                i.state = 'training_completed'
            if self.upaya_id.state == 'complete':
                i.state = 'complete'
            if self.upaya_id.state == 'cancel':
                i.state = 'cancel'
            if self.upaya_id.state == 'draft':
                i.state = 'draft'
            if self.upaya_id.state == 'training':
                i.state = 'training'
            if self.upaya_id.state == 'split':
                i.state = 'split'

    state = fields.Selection(
        [('draft', 'Draft'), ('training', 'Training'), ('training_completed', 'Training Completed'),
         ('split', 'Splitted'), ('confirm', 'Upaya Started'),
         ('complete', 'Completed'), ('cancel', 'Cancelled')],
        default='draft', string='Status', compute="_compute_onchange_state"
    )
