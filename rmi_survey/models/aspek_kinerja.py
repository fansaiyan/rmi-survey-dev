# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class AspekKinerja(models.Model):
    _name = "rmi.aspek_kinerja"
    _description = "Aspek Kinerja"

    name = fields.Char(string="Aspek")
    aspect_values = fields.Many2one('rmi.final_rating', string="Final Rating", required=True)
    composite_risk_levels = fields.Many2one('rmi.komposit_risiko', string="Peringkat Komposit Risiko", required=True)
    company_name = fields.Char(string="Company", compute="_compute_company_name", readonly=True)
    aspect_conversion_value = fields.Integer(string="Nilai Konversi", readonly=True, compute="_compute_final_rating")
    composite_risk_conversion_value = fields.Integer(
        string="Nilai Konversi",
        readonly=True,
        compute="_compute_composite_risk_level"
    )
    final_rating_weight = fields.Integer(string="Bobot Final Rating")
    composite_risk_weight = fields.Integer(string="Bobot Peringkat Komposit Risiko")
    conversion_rating_value = fields.Float(
        string="Nilai Konversi x Bobot Final Rating",
        readonly=True,
        compute="_compute_conversion_rating_value"
    )
    conversion_risk_value = fields.Float(
        string="Nilai Konversi x Bobot Risiko",
        readonly=True,
        compute="_compute_conversion_risk_value"
    )
    total_rating_value = fields.Float(
        string="Total Nilai",
        compute="_compute_total_rating_value"
    )
    score_adjustment = fields.Float(string="Penyesuain Skor", readonly=True)
    survey_ids = fields.Many2one('survey.survey', string="Survey")
    periode = fields.Char(string="Periode", readonly=True, related='survey_ids.periode')
    jenis_industri = fields.Selection(string="Jenis Industri", readonly=True, related='survey_ids.jenis_industri')
    state = fields.Selection([
                 ('new', 'New'),
                 ('done', 'Done'),
    ], default='new', tracking=True)
    aspek_corporate_ids = fields.One2many(
        'rmi.aspek_dimensi_corporate',
        'aspek_kinerja_ids',
        string="Aspek Kinerja Corporate",
        readonly=True
    )
    skor_aspek_dimensi = fields.Float(string="Skor Aspek Dimensi", readonly=True)
    is_aspek_dimensi = fields.Boolean(string="Aspek Dimensi Exist", readonly=True)
    skor_rmi_final = fields.Float(string="Skor RMI Final", readonly=True)
    no_laporan = fields.Char(string="Nomor Laporan", readonly=True)

    def generate_report(self):
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
        """.format(self.survey_ids.id)
        self.env.cr.execute(query_calculation)
        fetched_data = self.env.cr.fetchall()
        # _logger.info(fetched_data)
        table_existing = self.env['rmi.aspek_dimensi_corporate'].search([('survey_id', '=', self.survey_ids.id)])
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
                'survey_id': self.survey_ids.id,
                'aspek_kinerja_ids': self.id
            })

            # Sum the skor_dimensi
            total_skor_dimensi = sum(record[3] for record in fetched_data)

            # Calculate skor_aspek_dimensi
            skor_aspek_dimensi = total_skor_dimensi / len(fetched_data)
            self.skor_aspek_dimensi = skor_aspek_dimensi
            self.skor_rmi_final = skor_aspek_dimensi + self.score_adjustment
            if self.skor_aspek_dimensi <= 3:
                self.is_aspek_dimensi = False
            else:
                self.is_aspek_dimensi = True

        return self.env.ref('rmi_survey.report_penilaian_rmi').report_action(self)

    @api.model
    def create(self, vals):
        new_order = super(AspekKinerja, self).create(vals)

        current_time = datetime.now()
        dt_sequence = self.env['ir.sequence'].sudo().search(
            [('code', '=', 'rmi.survey')],
            limit=1
        )
        year = current_time.strftime('%y')
        month = current_time.strftime('%mm')
        next_number = dt_sequence.number_next
        formatted_number = str(next_number).zfill(2)
        sequence_prefix = formatted_number + "/"
        sequence_suffix = month + "/RMI/" + year

        no_laporan = sequence_prefix + sequence_suffix
        new_order.write({'no_laporan': no_laporan, 'state': 'done'})
        next_number += 1
        dt_sequence.write({
            'number_next': next_number
        })
        return new_order

    @api.onchange('final_rating_weight', 'aspect_values', 'composite_risk_levels')
    def _compute_conversion_rating_value(self):
        for record in self:
            record.conversion_rating_value = (record.aspect_conversion_value * record.final_rating_weight) / 100

    @api.onchange('composite_risk_weight', 'aspect_values', 'composite_risk_levels')
    def _compute_conversion_risk_value(self):
        for record in self:
            record.conversion_risk_value = (record.composite_risk_conversion_value * record.composite_risk_weight) / 100

    @api.depends('aspect_values')
    def _compute_final_rating(self):
        for record in self:
            record.aspect_conversion_value = record.aspect_values.nilai

    @api.depends('composite_risk_levels')
    def _compute_composite_risk_level(self):
        for record in self:
            record.composite_risk_conversion_value = record.composite_risk_levels.nilai

    @api.depends('conversion_rating_value', 'conversion_risk_value')
    def _compute_total_rating_value(self):
        for record in self:
            record.total_rating_value = record.conversion_rating_value + record.conversion_risk_value
            self.calculate_score_adjustment(record.total_rating_value)

    @api.depends('aspect_values')
    def _compute_company_name(self):
        for record in self:
            record.company_name = self.env.user.company_id.display_name

    @api.depends('total_rating_value')
    def calculate_score_adjustment(self, total_rating_value):
        if 0 < total_rating_value <= 50:
            self.score_adjustment = -1.00
        elif 50 < total_rating_value <= 65:
            self.score_adjustment = -0.75
        elif 65 < total_rating_value <= 80:
            self.score_adjustment = -0.50
        elif 80 < total_rating_value <= 90:
            self.score_adjustment = -0.25
        else:
            self.score_adjustment = 0.00

