# -*- coding: utf-8 -*-
{
    'name': "RMI Survey",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'marketing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','survey'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/aspek_kinerja.xml',
        'views/param_dimensi.xml',
        'views/param_group.xml',
        'views/final_rating.xml',
        'views/komposit_risiko.xml',
        'views/survey_inherit_view.xml'
    ]
}
