# -*- coding: utf-8 -*-

{
    'name': 'Cafe2',
    'application': True,
    'author': 'Dev Prajapati',
    'depends': ['mail'],
    # 'assets': {
    #     'web.assets_common': [
    #         'cafe/static/src/css/custom.css',
    #     ],
    # },
    # 'installable': True,
    'data': [
        # 'data/sale_order_number.xml',
        'security/ir.model.access.csv',
        'views/action.xml',
        'views/menu.xml',
        'views/views.xml'
    ],
    'summary': 'Practicing Odoo!'
}