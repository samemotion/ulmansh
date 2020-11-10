from odoo import api, exceptions, fields, models, _

import logging

_logger = logging.getLogger(__name__)

class ProductPackaging(models.Model):
	_inherit = "product.packaging"

	@api.model
	def create(self, vals):
		vals['barcode'] = self.env['ir.sequence'].next_by_code('product.packaging.barcode')
		product_packaging = super(ProductPackaging, self).create(vals)
		return product_packaging