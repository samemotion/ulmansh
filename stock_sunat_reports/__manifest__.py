# -*- coding: utf-8 -*-
# Part of Same Motion. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock SUNAT Reports',
    'version': '1.0',
    'category': 'Warehouse',
    'author': 'Same Motion',
    'description': """
This module adds SUNAT Stock Reports
=================================================================
    """,
    'website': 'https://www.samemotion.com',
    'depends': ['stock','l10n_pe_stock_base','product_type_pe','stock_operation_type','invoice_type'],
    'data': [
#        'security/ir.model.access.csv',
#        'views/stock_picking_batch_views.xml',
#        'data/stock_picking_batch_data.xml',
#        'wizard/stock_picking_to_batch_views.xml',
         'report/stock_sunat_report_view.xml',
         'report/stock_quantity_sunat_report.xml',
         'wizard/stock_report_loader.xml',
         'views/product.xml',
         'views/stock.xml',
         'data/product.uom.pe.csv',
         'data/data_stock_type_book.xml',
         'data/data_invoice_type.xml',
         'data/data_product_uom_type.xml',
    ],
    'demo': [
#        'data/stock_picking_batch_demo.xml',
    ],
    'installable': True,
}