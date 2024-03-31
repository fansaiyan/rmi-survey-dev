from odoo import models, fields, api

class AspekKinerja(models.Model):
    _name = "rmi.aspek_kinerja"
    _description = "Aspek Kinerja"

    name = fields.Char(string="Aspek", required=True)
    nilai_aspek = fields.Char(string="Nilai Aspek", required=True)
    nilai_konversi = fields.Integer(name="Nilai Konversi", required=True)
