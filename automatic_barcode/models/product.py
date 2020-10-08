from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta, date, datetime

class ProductCategory(models.Model):
    
    _inherit = "product.category"
    
    x_prefix = fields.Char(string="Prefix")
    
    
class ProductProduct(models.Model):
    
    _inherit = "product.product"
    
    @api.multi
    def action_generate_barcode(self):
        result = False
        for record in self:
            category_id = record.categ_id
            while True:
                if category_id:
                    result = category_id.x_prefix
                    if result:
                        break
                    else:
                        category_id = category_id.parent_id
                else:
                    result = False
                    return
            if not record.barcode:
                sequence = self.env['ir.sequence'].next_by_code('product.barcode.sequence')
                barcode = result + sequence
                record.barcode = barcode        
        return 
    