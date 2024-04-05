from odoo import models, fields, api


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
        compute="_compute_total_rating_value",
        readonly=True
    )
    score_adjustment = fields.Float(string="Penyesuain Skor", readonly=True)
    survey_ids = fields.Many2one('survey.survey', string="Survey")

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

    def final_save(self):
        print(self)
