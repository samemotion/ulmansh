# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import namedtuple
import json
import time

from itertools import groupby
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from operator import itemgetter

class Picking(models.Model):
    _inherit = "stock.picking"

    x_sale_order = fields.Many2one('Pedido de ventas')
    x_client_order_ref = fields.Char(string='Referencia del Cliente',
                               related='sale_id.client_order_ref')

    def _compute_get_module(self):
        module = self.env['ir.module.module'].sudo().search([('name', '=', 'l10n_pe_stock_epicking_outgoing')])
        if module.state == 'installed':
            if self.x_picking_is_electronic:
                self.module_x_picking_is_electronic = True    
                
                
    module_x_picking_is_electronic = fields.Boolean(compute="_compute_get_module", string="x_picking_is_electronic", default=False)                               

    @api.multi
    def action_print_picking_pe(self):
        """ Print the Guia de Remision, 
        """
        self.ensure_one()
        return self.env.ref('reports_ulman.printguiaremision_report').report_action(self)

        