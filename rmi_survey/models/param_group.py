from odoo import api, fields, models

class ParamGroup(models.Model):
    _name = 'rmi.param_group'
    _description = 'Parameter Group'

    name = fields.Char(string='Group Name', required=True)
    param_dimensi = fields.Many2one(
        comodel_name='rmi.param_dimensi',
        string='Parameter Dimensi',
        required=True
    )