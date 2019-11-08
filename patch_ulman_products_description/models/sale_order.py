from odoo import api, exceptions, fields, models, _

import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    @api.multi
    def _prepare_invoice_line(self, qty):

        res = super(SaleOrderLine,self)._prepare_invoice_line(qty)
        
        if self.product_id.type == 'product':
            
            res['name']=self.product_id.display_name
            
        elif self.product_id.type == 'service':
            
            res['name'] = self.name
               
        return res
    
    
        

    