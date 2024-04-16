# -*- coding: utf-8 -*-

import logging

from odoo import models, fields, api
_logger = logging.getLogger(__name__)


class SurveyInherit(models.Model):
    """inherited survey model"""
    _inherit = 'survey.survey'

    jenis_industri = fields.Selection([('umum', 'Umum'), ('perbankan', 'Perbankan'), ('asuransi', 'Asuransi')],
                                      'Jenis Industri', default='umum')
    periode = fields.Char(string='Periode')
    dashboard_id = fields.Many2one('rmi.survey_dashboard_aspect_dimension', string='Dashboard')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)

    def generate_adjust_aspect_dimension(self):
        # Execute custom SQL query
        query_aspek_dimensi = """
            select
                ROW_NUMBER() OVER () AS no,
                h.name as company,
                a.question_id as question_id,
                i.name as dimensi,
                j.name as subdimensi,
                (b.title->>'en_US')::varchar AS parameterName,
                avg((e.value->>'en_US')::int) as avgvalue,
                min((e.value->>'en_US')::int) as minvalue,
                max((e.value->>'en_US')::int) as maxvalue,
                max((e.value->>'en_US')::int) - min((e.value->>'en_US')::int) as rangevalue
                from survey_user_input_line as a
                left join survey_question as b on a.question_id = b.id
                left join survey_user_input as c on c.id = a.user_input_id
                left join res_partner as d on d.id = c.partner_id
                left join survey_question_answer as e on e.id = a.suggested_answer_id
                left join res_users as f on f.partner_id = d.id
                left join hr_employee as g on g.user_id = f.id
                left join res_company as h on h.id = g.company_id
                left join rmi_param_dimensi as i on i.id = b.dimensi_names
                left join rmi_param_group as j on j.id = b.sub_dimensi_names
            where a.survey_id = {} and c.state = 'done'
            GROUP BY a.question_id, parameterName, company, i.name, j.name
            ORDER BY a.question_id ASC
        """.format(self.id)
        self.env.cr.execute(query_aspek_dimensi)
        fetched_data = self.env.cr.fetchall()
        # _logger.info(fetched_data)
        # Iterate over fetched_data and create records
        table_existing = self.env['rmi.survey_dashboard_aspect_dimension'].search([('survey_id', '=', self.id)])
        if table_existing:
            # Delete the record
            table_existing.unlink()
        for record_data in fetched_data:
            # Create a new record
            self.env['rmi.survey_dashboard_aspect_dimension'].create({
                'no': record_data[0],
                'company': record_data[1],
                'question_id': record_data[2],
                'dimension': record_data[3],
                'sub_dimension': record_data[4],
                'parameter_name': record_data[5],
                'avg_value': record_data[6],
                'min_value': record_data[7],
                'max_value': record_data[8],
                'range_value': record_data[9],
                'name': self.title,
                'survey_id': self.id
                # Add more fields as needed
            })

        self.ensure_one()
        result = self.env['ir.actions.act_window']._for_xml_id('rmi_survey.survey_dashboard_dimension_action')
        return result

    def generate_graph(self):
        # Execute custom SQL query
        query_calculation = """
            select
                CASE
                    WHEN f.name = 'Budaya dan Kapabilitas Risiko' THEN '1 s.d. 3'
                    WHEN f.name = 'Organisasi dan Tata Kelola Risiko' THEN '4 s.d. 19'
                    WHEN f.name = 'Kerangka Risiko dan Kepatuhan' THEN '20 s.d. 33'
                    WHEN f.name = 'Proses dan Kontrol Risiko' THEN '34 s.d. 39'
                    ELSE '40 s.d. 42'
                END as parameter,
                ROW_NUMBER() OVER () AS dimensi,
                f.name as deskripsi,
                TRUNC(avg((e.value->>'en_US')::int) * 10) / 10.0 AS skordimensi
                from survey_user_input_line as a
                left join survey_question as b on a.question_id = b.id
                left join survey_user_input as c on c.id = a.user_input_id
                left join res_partner as d on d.id = c.partner_id
                left join survey_question_answer as e on e.id = a.suggested_answer_id
                left join rmi_param_dimensi as f on f.id = b.dimensi_names
                left join rmi_param_group as g on g.id = b.sub_dimensi_names
            where a.survey_id = {}
            group by f.name, f.id
            order by f.id asc
        """.format(self.id)
        self.env.cr.execute(query_calculation)
        fetched_data = self.env.cr.fetchall()
        # _logger.info(fetched_data)
        table_existing = self.env['rmi.aspek_dimensi_corporate'].search([('survey_id', '=', self.id)])
        if table_existing:
            # Delete the record
            table_existing.unlink()
        for record_data in fetched_data:
            # Create a new record
            self.env['rmi.aspek_dimensi_corporate'].create({
                'parameter': record_data[0],
                'dimensi': record_data[1],
                'deskripsi': record_data[2],
                'skor_dimensi': record_data[3],
                'survey_id': self.id
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'rmi_survey.rmi_dashboard'
        }


class SurveyQuestionInherit(models.Model):
    """inherited survey question """
    _inherit = 'survey.question'

    dimensi_names = fields.Many2one('rmi.param_dimensi', 'Nama Dimensi')
    sub_dimensi_names = fields.Many2one('rmi.param_group', 'Nama Sub Dimensi',
                                        domain="[('param_dimensi', '=', dimensi_names)]")
    document_ids = fields.One2many(
        comodel_name='rmi.documents',
        inverse_name='survey_ids',
        string='Documents',
        required=False
    )

    @api.onchange('dimensi_names')
    def _onchange_dimension_id(self):
        if self.sub_dimensi_names:
            self.sub_dimensi_names = False


class HrEmployeeInherit(models.Model):
    """inherited hr employee """
    _inherit = "hr.employee"

    branch_id = fields.Many2one("res.branch", string='Default Branch')
