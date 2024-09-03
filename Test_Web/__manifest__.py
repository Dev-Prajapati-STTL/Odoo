{
    'name':'Test Website',
    'application': True,
    'category': 'Website',
    'depends':[
        'website', 'website_sale'
    ],
    'data':[
        'data/menu.xml',    
        'data/pages.xml',   
        'views/custom_pages.xml',
        'views/inherit_button.xml',
    ]
}