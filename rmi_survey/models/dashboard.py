from odoo import fields, models, api


class Dashboard(models.Model):
    _name = 'rmi.survey_dashboard'
    _description = 'Dashboard RMI Survey Model'

    name = fields.Char()


class DashboardAspectDimension(models.Model):
    _name = 'rmi.survey_dashboard_aspect_dimension'
    _description = 'Dashboard RMI Survey Aspect Dimension Model'

    name = fields.Char()
    no = fields.Integer(string='No')
    company = fields.Char(string='Company')
    question_id = fields.Many2one('survey.question', string='Question')
    parameter_name = fields.Char(string='Parameter Name')
    avg_value = fields.Float(string='Average Value')
    min_value = fields.Float(string='Minimum Value')
    max_value = fields.Float(string='Maximum Value')
    range_value = fields.Float(string='Range Value')
    survey_id = fields.Many2one('survey.survey', string='Survey ID')


