from odoo import fields, models, api


class Documents(models.Model):
    _name = 'rmi_survey.documents'
    _description = 'Bukti dokumen RMI Survey Model'

    name = fields.Char('Nama Dokumen', required=True)
    description = fields.Text('Deskripsi')
    files = fields.Binary(
        string='Files',
    )
