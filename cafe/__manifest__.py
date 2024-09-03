# -*- coding: utf-8 -*-

{
    'name': 'Cafe',
    'application': True,
    'author': 'Dev Prajapati',
    'assets': {
        'web.assets_common': [
            'cafe/static/src/css/custom.css',
        ],
    },
    'installable': True,
    'data': [
        'data/sale_order_number.xml',
        'security/ir.model.access.csv',
        'views/action.xml',
        'views/menu.xml',
        'views/views.xml',
        'report/report_action.xml',
        'report/report_template.xml'
    ],
    'summary': 'Practicing Odoo!'
}
