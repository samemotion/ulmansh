# -*- coding: utf-8 -*-
{
    'name': "fix problem product description",

    'summary': """
    Fix product description.
    """,

    'description': """
    Fix product description.
    """,

    'author': "Same Motion",
    'website': "http://www.samemotion.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '1.6',
    'depends': ['sale','sale_stock','l10n_pe_stock_base','l10n_pe_refund_sales_order_fix'],
    'data': [
#         'views/stock_picking_views.xml',
        ],
    'demo': [
    ],
}
