from odoo import api, fields, models


class ParamDimensi(models.Model):
    _name = 'rmi.param_dimensi'
    _description = 'Parameter Dimensi'

    name = fields.Char(string="Dimensi Name", required=True)
    param_dimensi_id = fields.Integer(string="Dimensi ID", required=True)
    param_groups = fields.One2many(
        comodel_name='rmi.param_group',
        inverse_name='param_dimensi',
        string='Parameter Group'
    )
