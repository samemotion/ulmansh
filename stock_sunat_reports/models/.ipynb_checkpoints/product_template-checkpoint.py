from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    x_product_type_pe = fields.Many2one('product.type.pe', string='Product Type Peru', help='Product Type - Peru', default=lambda self: self.env['product.type.pe'].search([], limit=1))
