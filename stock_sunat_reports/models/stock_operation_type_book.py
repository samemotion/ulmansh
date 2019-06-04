from odoo import api, fields, models, _

class StockOperationTypeBook(models.Model):
    _name = 'stock.operation.type.book'
    _description = "stock operation type table for sunat books"
    
    x_name = fields.Char(string = 'Name')
    x_code = fields.Char(string  = 'Code')
