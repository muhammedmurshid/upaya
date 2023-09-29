from odoo import models, fields, api, _


class UpayaSkills(models.Model):
    _name = 'upaya.skills'
    _description = 'Upaya Skills'

    name = fields.Char('Name')
    student_id = fields.Integer()
    skill_id = fields.Many2one('upaya.form', string="Skills")
    communication_skill = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        default='1', string='Communication Skill')
    language_skill = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Language Skill', default='1',
    )
    presentation_skill = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Presentation Skill', default='1',
    )
    confidence_level = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Confidence Level', default='1',
    )
    body_language = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Body Language', default='1',
    )
    dressing_pattern = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Dressing Pattern', default='1',
    )
    attitude = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Attitude', default='1',
    )
    friendliness = fields.Selection(
        [('0', 'None'), ('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Very Good'), ('5', 'Excellent')],
        string='Friendliness', default='1',
    )

    @api.depends('communication_skill', 'presentation_skill', 'language_skill', 'confidence_level', 'body_language',
                  'dressing_pattern', 'attitude', 'friendliness')
    def _compute_total_score(self):
        for rec in self:

            vars1 = int(rec.communication_skill)
            var2 = int(rec.presentation_skill)
            var3 = int(rec.language_skill)
            var4 = int(rec.confidence_level)
            var5 = int(rec.body_language)
            var6 = int(rec.dressing_pattern)
            var7 = int(rec.attitude)
            var8 = int(rec.friendliness)
            if var8 or var7 or var6 or var5 or var4 or var3 or var2 or var1:
                aa = vars1 + var2 + var3 + var4 + var5 + var6 + var7 + var8
                rec.write({'total_score': aa})
            else:
                aa = 0
            # aa = vars1 + var2 + var3 + var4 + var5 + var6 + var7 + var8
            # print(aa, 'total')
            # self.write({'total_score': aa})

    total_score = fields.Float('Total Score', compute='_compute_total_score', store=True)
