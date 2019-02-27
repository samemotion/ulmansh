# -*- coding: utf-8 -*-
{
    'name': "POS Ticket Fix",

    'summary': """
        POS Ticket Fix""",

    'description': """
        POS Ticket Fix
        - 
    """,

    'author': "Same Motion",

    'website': "http://www.samemotion.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Localization',
    'version': '3.0',

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    # always loaded
    'data': [
        'views/template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
 #       'demo/demo.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],
}