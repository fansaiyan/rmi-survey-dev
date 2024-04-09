from odoo import fields, models, api


class Dashboard(models.Model):
    _name = 'rmi.survey_dashboard'
    _description = 'Dashboard RMI Survey Model'

    name = fields.Char()
