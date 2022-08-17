# -*- encoding: utf-8 -*-
{
    'name': "Row Number in tree purchase and sales",
    'version': '14.0.1.1',
    'summary': 'Show row number in tree purchase and sales.',
    'category': 'Other',
    'description': """""",
    "depends": ['web', 'sale', 'purchase'],
    'data': [
        'views/listview_templates.xml',
        'report/sale_order.xml',
        'report/purchase_order.xml'
    ],
    "images": [],
    'license': 'LGPL-3',

    # Author
    'author': 'Pragmatic S.A.C',
    'website': 'https://www.pragmatic.com.pe/',
    'maintainer': 'Pragmatic S.A.C',

    'qweb': [
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
