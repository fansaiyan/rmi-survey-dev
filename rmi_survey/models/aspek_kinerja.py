from odoo import models, fields, api


class AspekKinerja(models.Model):
    _name = "rmi.aspek_kinerja"
    _description = "Aspek Kinerja"

    name = fields.Char(string="Aspek")
    aspect_values = fields.Many2one('rmi.final_rating', string="Final Rating", required=True)
    composite_risk_levels = fields.Many2one('rmi.komposit_risiko', string="Peringkat Komposit Risiko", required=True)
    company_name = fields.Char(string="Company")
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
    total_rating_value = fields.Float(string="Total Nilai", compute="_compute_total_rating_value", readonly=True)

    @api.onchange('final_rating_weight')
    def _compute_conversion_rating_value(self):
        for record in self:
            record.conversion_rating_value = (record.aspect_conversion_value * record.final_rating_weight) / 100

    @api.onchange('composite_risk_weight')
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

    def final_save(self):
        print(self)
