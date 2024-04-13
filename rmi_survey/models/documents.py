from odoo import fields, models, api


class Documents(models.Model):
    _name = 'rmi.documents'
    _description = 'Bukti dokumen RMI Survey Model'

    name = fields.Char('Nama Dokumen', required=True)
    # description = fields.Text('Deskripsi')
    files = fields.Binary(
        string='Files',
    )
    survey_ids = fields.Many2one(
        comodel_name='survey.question',
        string='Survey Ids',
        readonly='1',
        required=False
    )
