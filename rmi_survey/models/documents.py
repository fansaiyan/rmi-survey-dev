from odoo import fields, models, api


class Documents(models.Model):
    _name = 'rmi.documents'
    _description = 'Bukti dokumen RMI Survey Model'

    name = fields.Char('Nama Dokumen', required=True)
    survey_ids = fields.Many2one(
        comodel_name='survey.question',
        string='Survey Ids',
        readonly='1',
        required=False
    )
    user_id = fields.Many2one('res.users', string='User Id', default=lambda self: self.env.user)
    link_url = fields.Char(string='Link URL', required=True)
