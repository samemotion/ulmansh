from odoo import models, fields, api

class ProductUoM(models.Model):
    _inherit = 'product.uom'

      ### This is when using electronics book  not supported on ulman now ### 
      # x_code_pe = fields.Many2one('product.uom.pe',string = 'Code Peru',help='Unit of Measure Code - Peru')
    
    ## For manual books
    x_code_pe = fields.Many2one('product.uom.type.book', string="Code Peru", help="Unit of Measure Code - Peru")

class ProductUoMPeru(models.Model):
    
    _name='product.uom.pe'
    _description='Units of measures according to peruvian regulations'

    x_code = fields.Char(string = "Code")
    x_name = fields.Char(string = "Name")