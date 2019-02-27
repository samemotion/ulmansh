# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'


    @api.multi
    def get_invoice_info(self, attributes):
        reference = attributes[0]
        order = self.env['pos.order'].search([('pos_reference', '=', reference)])
        invoice = order.invoice_id
        number = str(invoice.x_document_serial) + '-' + str(invoice.x_document_correlative)
        create_date = invoice.create_date
        qr_code = 'data:image/png;base64,' + invoice.x_qr_invoice.decode('ascii')
        qr_link = self.env['ir.config_parameter'].get_param('web.base.url') + '/einvoicing_get_document'
        change = 0

        lines = []
        for line in invoice.invoice_line_ids:
            # taxes = 1
            # for t in line.invoice_line_tax_ids:
            #     taxes = taxes * (1 + t.amount/100)

            lines.append({
                'quantity': line.quantity,
                'description': line.product_id.name,
                'price_unit': line.price_unit,
                'subtotal': line.price_unit * line.quantity,
            })

        statements = []
        for d in order.statement_ids:
            if d.amount > 0:
                statements.append({
                    'name': d.journal_id.name,
                    'amount': d.amount
                })
            if d.amount < 0:
                change = abs(d.amount)

        return {
            'number': number, 
            'create_date': create_date, 
            'qr_code': qr_code, 
            'lines': lines,
            'qr_link': qr_link,
            'statements': statements,
            'change': change,
            'currency_symbol': order.invoice_id.currency_id.symbol,
            'currency_description': order.invoice_id.currency_id.x_description,
            'business_name': order.invoice_id.company_id.partner_id.x_business_name,
            'street': order.invoice_id.partner_id.company_id.street
        }