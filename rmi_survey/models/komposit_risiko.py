from odoo import api, fields, models

class KompositRisko(models.Model):
    _name = 'rmi.komposit_risiko'
    _description = 'Kompisit Risko'

    name = fields.Char(string='Peringkat Komposit Risko', required=True)
    nilai = fields.Integer(string='Nilai Konversi', required=True)
