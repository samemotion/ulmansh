# -*- coding: utf-8 -*-
{
    'name': "TaxType Patch",

    'summary': """
    TaxType Patch.
    """,

    'description': """
    TaxType Patch.
    """,

    'author': "Same Motion",
    'website': "http://www.samemotion.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'electronic invoice',
    'version': '0.1',
    #'depends': ['sale','sale_stock','l10n_pe_stock_base'],
    'data': [
        'data/tax_type_code.xml',
        'data/exemption_code.xml',
        ],
    'demo': [
    ],
}
