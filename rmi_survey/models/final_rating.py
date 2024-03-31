from odoo import models, fields, api

class FinalRating(models.Model):
    _name = 'rmi.final_rating'
    _description = 'Final Rating'

    name = fields.Char(string='Peringkat Akhir', required=True)
    nilai = fields.Integer(string='Nilai Konversi', required=True)