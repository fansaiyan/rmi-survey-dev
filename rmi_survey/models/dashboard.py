from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


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
    aspect_ids = fields.One2many(
        comodel_name='rmi.detail_survey_aspect_dimension',
        inverse_name='dimension_ids',
        string='Aspect ID',
        required=False
    )

    def get_table_detail(self):
        # Execute custom SQL query
        query_detail = """
        select
            ROW_NUMBER() OVER () AS No,
            a.question_id,
            h.name as company,
            (b.title->>'en_US')::varchar AS parameterName,
            d.name as user,
            i.name as Department,
            (e.value->>'en_US')::int AS value
            from survey_user_input_line as a
            left join survey_question as b on a.question_id = b.id
            left join survey_user_input as c on c.id = a.user_input_id
            left join res_partner as d on d.id = c.partner_id
            left join survey_question_answer as e on e.id = a.suggested_answer_id
            left join res_users as f on f.partner_id = d.id
            left join hr_employee as g on g.user_id = f.id
            left join res_company as h on h.id = g.company_id
            left join hr_department as i on i.id = g.department_id
        where a.survey_id = {} and c.state = 'done' and a.question_id = {}
        """.format(self.survey_id.id, self.question_id.id)
        self.env.cr.execute(query_detail)
        fetched_data = self.env.cr.fetchall()
        table_existing = self.env['rmi.detail_survey_aspect_dimension'].search([('dimension_ids', '=', self.id)])
        if table_existing:
            # Delete the record
            table_existing.unlink()
        for data in fetched_data:
            # Create a new record
            self.env['rmi.detail_survey_aspect_dimension'].create({
                'no': data[0],
                'question_id': data[1],
                'company': data[2],
                'parameter_name': data[3],
                'user': data[4],
                'department': data[5],
                'value': data[6],
                'name': self.survey_id.title,
                'survey_id': self.survey_id.id,
                'dimension_ids': self.id
            })
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload'
        # }


class DetailAspectDimension(models.Model):
    _name = 'rmi.detail_survey_aspect_dimension'
    _description = 'RMI Survey Detail Aspect Dimension Model'

    name = fields.Char(readonly=True)
    no = fields.Integer(string='No', readonly=True)
    company = fields.Char(string='Company', readonly=True)
    question_id = fields.Many2one('survey.question', string='Question', readonly=True)
    parameter_name = fields.Char(string='Parameter Name', readonly=True)
    value = fields.Integer(string='Value', readonly=True)
    user = fields.Char(string='User', readonly=True)
    department = fields.Char(string="Department", readonly=True)
    survey_id = fields.Many2one('survey.survey', string='Survey ID', readonly=True)
    dimension_ids = fields.Many2one(
        comodel_name='rmi.survey_dashboard_aspect_dimension',
        string='Dimension Ids',
        readonly='1',
        required=False
    )
