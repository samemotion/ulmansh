from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    x_product_type_pe = fields.Many2one('product.type.pe', related='product_tmpl_id.x_product_type_pe' ,string='Product Type Peru', help='Product Type - Peru', default=lambda self: self.env['product.type.pe'].search([], limit=1))
