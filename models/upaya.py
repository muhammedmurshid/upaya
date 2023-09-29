from odoo import models, api, fields, _
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta


class UpayaForm(models.Model):
    _name = 'upaya.form'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Upaya Form'

    name = fields.Char('Name')

    batch_id = fields.Many2one('logic.base.batch', string='Batch', required=True)
    date = fields.Date('Upaya Date', required=True)
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    batch_start_date = fields.Date('Batch Start Date', )
    batch_end_date = fields.Date('Batch End Date', )
    subject_for_presentation = fields.Char('Subject For Presentation')
    state = fields.Selection(
        [('draft', 'Draft'), ('training', 'Training'), ('training_completed', 'Training Completed'),
         ('split', 'Splitted'), ('confirm', 'Upaya Started'),
         ('complete', 'Completed'), ('cancel', 'Cancelled')],
        default='draft', string='Status',
    )
    type = fields.Selection([('case_study', 'Case Study'), ('topic_presentation', 'Topic Presentation')], string='Type')
    upaya_attendance_ids = fields.One2many('upaya.students.attendance', 'upaya_id')
    coordinator_id = fields.Many2one('res.users', string='Coordinator', related='batch_id.academic_coordinator')
    display_name = fields.Char(compute='_compute_display_name', store=True)
    # pro_coordinator_id = fields.Many2one('res.users', string='Programme Coordinator',
    #                                      default=lambda self: self.env.user)
    skills_ids = fields.One2many('upaya.skills', 'skill_id')

    def training_start(self):
        self.state = 'training'

    def action_team_split(self):
        students = []
        print('kjsdghhfsadatiyrgherieur')
        std = self.env['upaya.teams'].search([])
        for i in std:
            for rec in self.upaya_attendance_ids:
                students.clear()
                res_list = {
                    'student_id': rec.student_id,
                }

                if rec.team_id.id == i.id:
                    students.append((0, 0, res_list))
                    i.write({
                        'teams_ids': students,
                    })
        print(students, 's')
        self.state = 'split'
        for stud in self.upaya_attendance_ids:
            if not stud.team_id:
                raise UserError("Please Add Specific Team For Each Student")

    def action_start_upaya(self):
        students = self.env['logic.students'].search([('batch_id', '=', self.batch_id.id)])
        abc = []
        unlink_commands = [(3, child.id) for child in self.skills_ids]
        self.write({'skills_ids': unlink_commands})

        for i in students:
            res_list = {
                'name': i.name,
                'student_id': i.id,

            }
            abc.append((0, 0, res_list))
        self.skills_ids = abc
        self.state = 'confirm'

    @api.onchange('batch_id')
    def _compute_display_name(self):
        for rec in self:
            if rec.batch_id:
                rec.display_name = rec.batch_id.name + ' - ' + 'Upaya'

    @api.onchange('batch_id')
    def onchange_batch_id(self):
        batch = self.env['logic.base.batch'].search([('id', '=', self.batch_id.id)])
        self.batch_start_date = batch.from_date
        self.batch_end_date = batch.to_date

    @api.onchange('date', 'batch_id')
    def onchange_date(self):
        if self.date and self.batch_end_date and self.batch_start_date:
            if not self.batch_start_date <= self.date <= self.batch_end_date:
                raise UserError("Date is not within the specified range.")

    def action_confirm(self):
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('upaya.mail_activity_upaya_form').id)])
        if self.state == 'submit':
            activity_id.action_feedback(feedback=f'Upaya Confirmed')

        other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('upaya.mail_activity_upaya_form').id)])
        other_activity_ids.unlink()
        self.state = 'confirm'

    @api.depends('make_visible_academic_head', 'batch_id')
    def _compute_academic_head_upaya(self):
        res_user = self.env['res.users'].search([('id', '=', self.env.user.id)])
        if res_user.has_group('upaya.upaya_head'):
            self.make_visible_academic_head = True

        else:
            self.make_visible_academic_head = False

    make_visible_academic_head = fields.Boolean(string="User", compute='_compute_academic_head_upaya')

    def action_submit(self):
        self.state = 'training_completed'

    def action_complete(self):
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('upaya.mail_activity_upaya_form').id)])
        if self.state == 'confirm':
            activity_id.action_feedback(feedback=f'Upaya Completed')

        other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('upaya.mail_activity_upaya_form').id)])
        other_activity_ids.unlink()
        students_score = []
        print('kjsdghhfsadatiyrgherieur')
        std = self.env['upaya.teams.students'].search([])
        for i in std:
            for rec in self.skills_ids:
                if rec.student_id == i.student_id.id:
                    print('ya')
                    i.write({
                        'student_score': rec.total_score,
                    })
        self.write({'state': 'complete'})

        record_teams = self.env['upaya.teams'].search([], order='total_team_score desc', limit=1).total_team_score
        print(record_teams, 'winner')
        winner = self.env['upaya.teams'].search([('total_team_score', '=', record_teams)])
        for win in winner:
            self.write(
                {'winner_id': [(4, win.id)]}
                       )
        # print(winner.name, 'winner')
        # self.winner_id = winner.id

    winner_id = fields.Many2many('upaya.teams', string='Winner')

        # record = record_teams.search([], order='total_team_score desc', limit=1).total_team_score)
        # print(record_teams.name, 'winner')

    @api.onchange('batch_id')
    def onchange_batch_id_for_attendance(self):
        print('kkk')
        record_teams = self.env['upaya.teams'].search([], order='total_team_score desc', limit=1).total_team_score
        print(record_teams.name, 'winner')

    def action_cancel(self):
        activity_id = self.env['mail.activity'].search([('res_id', '=', self.id), ('user_id', '=', self.env.user.id), (
            'activity_type_id', '=', self.env.ref('upaya.mail_activity_upaya_form').id)])
        if self.state == 'confirm':
            activity_id.action_feedback(feedback=f'Upaya Cancelled')

        other_activity_ids = self.env['mail.activity'].search([('res_id', '=', self.id), (
            'activity_type_id', '=', self.env.ref('upaya.mail_activity_upaya_form').id)])
        other_activity_ids.unlink()
        self.state = 'cancel'

    @api.onchange('batch_id')
    def onchange_batch_id_for_attendance(self):
        students = self.env['logic.students'].search([('batch_id', '=', self.batch_id.id)])
        abc = []
        unlink_commands = [(3, child.id) for child in self.upaya_attendance_ids]
        self.write({'upaya_attendance_ids': unlink_commands})

        for i in students:
            res_list = {
                'name': i.name,
                'student_id': i.id,

            }
            abc.append((0, 0, res_list))
        self.upaya_attendance_ids = abc

    def create_send_activity_users(self):
        today = fields.Datetime.now()

        ss = self.env['upaya.form'].search([])
        # if jj.state not in 'confirm':
        #     jj.state_bool = True
        for i in ss:
            if i.state == 'confirm':
                date_1_days_later = i.date + timedelta(days=1)
                if date_1_days_later == today.date():
                    users = ss.env.ref('upaya.upaya_hr').users
                    for j in users:
                        i.activity_schedule('upaya.mail_activity_upaya_form', user_id=j.id,
                                            note=f'Delayed: Upaya is running behind schedule.')

    def coordinator_alert_message(self):
        today = fields.Datetime.now()
        one_day_before = datetime.now().date() - timedelta(days=1)
        print(one_day_before, 'before')
        ss = self.env['upaya.form'].search([])
        activities_to_remind = self.env['upaya.form'].search([('date', '=', one_day_before)])
        print(activities_to_remind, 'activities_to_remind')
        # if jj.state not in 'confirm':
        #     jj.state_bool = True
        for i in activities_to_remind:
            if i.state == 'submit':
                users = ss.env.ref('upaya.upaya_coordinator').users
                for j in users:
                    i.activity_schedule('upaya.mail_activity_upaya_form', user_id=j.id,
                                        note=f'Tomorrow: Upaya reminder.')



    # @api.model
    # def action_share(self):
    #     print('kkk')


class UpayaTeams(models.Model):
    _name = 'upaya.teams'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Teams'

    name = fields.Char('Name', required=True)
    topic_for_presentation = fields.Char('Topic For Presentation', required=True)
    teams_ids = fields.One2many('upaya.teams.students', 'team_student_id')

    @api.depends('teams_ids.student_score')
    def _compute_total_score(self):
        for rec in self:
            total = 0
            for score in rec.teams_ids:
                total += score.student_score
            rec.update({
                'total_team_score': total,
            })

    total_team_score = fields.Float(string='Total Score', compute='_compute_total_score', store=True)


class TeamsStudents(models.Model):
    _name = 'upaya.teams.students'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Teams Students'

    student_id = fields.Many2one('logic.students')
    student_score = fields.Float('Score')
    team_student_id = fields.Many2one('upaya.teams')
