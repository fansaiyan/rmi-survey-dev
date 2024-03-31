# -*- coding: utf-8 -*-
# from odoo import http


# class RmiSurvey(http.Controller):
#     @http.route('/rmi_survey/rmi_survey', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rmi_survey/rmi_survey/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rmi_survey.listing', {
#             'root': '/rmi_survey/rmi_survey',
#             'objects': http.request.env['rmi_survey.rmi_survey'].search([]),
#         })

#     @http.route('/rmi_survey/rmi_survey/objects/<model("rmi_survey.rmi_survey"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rmi_survey.object', {
#             'object': obj
#         })
