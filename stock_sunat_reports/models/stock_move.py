# -*- coding: utf-8 -*-
from odoo.addons import decimal_precision as dp
from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    x_warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse',help="Warehouse related to stock move line",store=True,compute='_compute_warehouse') 
    
    @api.one
    @api.depends('location_dest_id','location_id')
    def _compute_warehouse(self):
        result = []
        if self.location_id.usage == "internal":
            result =  self.location_id.x_warehouse_id
        if self.location_dest_id.usage == "internal":
            result =  self.location_dest_id.x_warehouse_id
        self.x_warehouse_id = result