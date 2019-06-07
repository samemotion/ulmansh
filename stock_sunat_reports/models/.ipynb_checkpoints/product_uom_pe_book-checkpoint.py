from odoo import api, fields, models, _

class ProductUomBook(models.Model):
    _name = 'product.uom.type.book'
    _description = 'Units of measures according peruvian regulations on book reports'
    
    x_name = fields.Char(string = 'Name')
    x_code = fields.Char(string  = 'Code')
    
    
