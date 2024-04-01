# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SurveyInherit(models.Model):
    _inherit = 'survey.survey'

    jenis_industri = fields.Selection([('umum', 'Umum'), ('perbankan', 'Perbankan'), ('asuransi', 'Asuransi')],
                                      'Jenis Industri', default='umum')


class SurveyQuestionInherit(models.Model):
    _inherit = 'survey.question'

    dimensi_names = fields.Many2one('rmi.param_dimensi', 'Nama Dimensi')
    sub_dimensi_names = fields.Many2one('rmi.param_group', 'Nama Sub Dimensi',
                                        domain="[('param_dimensi', '=', dimensi_names)]")

    @api.onchange('dimensi_names')
    def _onchange_dimension_id(self):
        if self.sub_dimensi_names:
            self.sub_dimensi_names = False
