from odoo import models, fields, api

class ProductUoM(models.Model):
    _inherit = 'product.uom'

    x_code_pe = fields.Many2one('product.uom.pe',string = 'Code Peru',help='Unit of Measure Code - Peru')

class ProductUoMPeru(models.Model):
    _name='product.uom.pe'
    _description='Units of measures according to peruvian regulations'

    x_code = fields.Char(string = "Code")
    x_name = fields.Char(string = "Name")