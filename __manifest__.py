# -*- coding: utf-8 -*-
{
    'name': "limite_credito",

    'summary': """
        Modulo que lleva el control del limite de credito""",

    'description': """
        Modulo que lleva el control del limite de credito
    """,

    'author': "Rodolfo Borstcheff",
    'website': "http://www.aquih.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/partner_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}