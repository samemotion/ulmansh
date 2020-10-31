# -*- coding: utf-8 -*-
{
    'name': "Automatic Barcode for Products",

    'summary': """
    """,

    'description': """
    Creates the barcode based on a prefix that comes from the category and a sequence from '000000001 
    """,

    'author': "Same Motion",
    'website': "http://www.samemotion.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Products',
    'version': '1.0',
    'depends': ['product'],
    'data': [
        'data/sequence_data.xml',
        'data/server_action_data.xml',
        'views/product_category_view.xml',
        'views/product_product_view.xml'
        ],
    'demo': [
    ],
}
