# -*- coding: utf-8 -*-
{
    'name': "Ulman's Reports",

    'summary': """
    Customizaed Invoice Reports.
    """,

    'description': """

    """,

    'author': "Same Motion",
    'website': "http://www.samemotion.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Reports',
    'version': '4.1',
    'depends': ['account'],
    'data': [
        'report/layout_templates.xml',
        'report/report_templates.xml',
        'report/custom_templates.xml',
        ],
    'demo': [
    ],
    'application': False,
}
