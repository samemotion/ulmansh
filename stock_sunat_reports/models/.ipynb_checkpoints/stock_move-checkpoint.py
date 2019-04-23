# -*- coding: utf-8 -*-
from odoo.addons import decimal_precision as dp
from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    
    x_warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse',help="Warehouse related to stock move line",store=True,compute='_compute_warehouse') 
    x_move_date = fields.Datetime(string='Move Date', help='When the move took place',compute='_get_move_date')
    x_operation_type = fields.Many2one('stock.operation.type',string='Operation Type',compute='_get_operation_type',store=False)
    
    @api.one
    @api.depends('location_dest_id','location_id')
    def _compute_warehouse(self):
        result = []
        if self.location_id.usage == "internal":
            result =  self.location_id.x_warehouse_id
        if self.location_dest_id.usage == "internal":
            result =  self.location_dest_id.x_warehouse_id
        self.x_warehouse_id = result
        
    @api.depends('picking_id','inventory_id')
    def _get_move_date(self):
        for record in self:
            if record.picking_id:
                record.x_move_date = record.picking_id.x_move_date
            elif record.inventory_id:
                record.x_move_date = record.inventory_id.date
            else:
                record.x_move_date = record.date
                
#Override Odoo
    def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id):
        self.ensure_one()
        AccountMove = self.env['account.move']
        quantity = self.env.context.get('forced_quantity', self.product_qty)
        quantity = quantity if self._is_in() else -1 * quantity

        # Make an informative `ref` on the created account move to differentiate between classic
        # movements, vacuum and edition of past moves.
        ref = self.picking_id.name
        if self.env.context.get('force_valuation_amount'):
            if self.env.context.get('forced_quantity') == 0:
                ref = 'Revaluation of %s (negative inventory)' % ref
            elif self.env.context.get('forced_quantity') is not None:
                ref = 'Correction of %s (modification of past move)' % ref

        move_lines = self.with_context(forced_ref=ref)._prepare_account_move_line(quantity, abs(self.value), credit_account_id, debit_account_id)
        if move_lines:
            date = self._context.get('force_period_date', fields.Date.context_today(self))
            new_account_move = AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': ref,
                'stock_move_id': self.id,
#Start Override
                'x_document_date':self.picking_id.x_move_date or date,
                'x_ple_state':self.picking_id._get_ple_state(self.picking_id.x_ple_state,self.picking_id.x_move_date,str(date) + " 00:00:00" ),
#End Override
            })
            new_account_move.post()

    @api.depends('picking_id','inventory_id','location_dest_id','location_id')
    def _get_operation_type(self):
        operation_type = ''
        for record in self:
            #To Production
            if record.location_id.usage == 'internal' and record.location_dest_id.usage == 'production':
                operation_type = self.env['stock.operation.type'].search([('x_code','=','10')])
            #From Production
            elif record.location_id.usage == 'production' and record.location_dest_id.usage == 'internal':
                operation_type = self.env['stock.operation.type'].search([('x_code','=','19')])
            elif (record.location_dest_id.usage == 'internal' and record.location_id.usage == 'inventory') or (record.location_dest_id.usage == 'inventory' and record.location_id.usage == 'internal'):
                # Inventory Adjustments - > Scrap
                if record.location_dest_id.scrap_location:
                    operation_type = self.env['stock.operation.type'].search([('x_code','=','13')])
                # Inventory Adjustments.
                else:
                    operation_type = self.env['stock.operation.type'].search([('x_code','=','28')])
            #Output -> Between Company Warehouses
            elif record.location_dest_id.usage == 'transit' and record.location_id.usage == 'internal':
                operation_type = self.env['stock.operation.type'].search([('x_code','=','11')])
            #Input -> Between Company Warehouses
            elif record.location_dest_id.usage == 'internal' and record.location_id.usage == 'transit':
                operation_type = self.env['stock.operation.type'].search([('x_code','=','19')])
            else:
                if record.picking_id:
                    operation_type = record.picking_id.x_operation_type
            record.x_operation_type = operation_type