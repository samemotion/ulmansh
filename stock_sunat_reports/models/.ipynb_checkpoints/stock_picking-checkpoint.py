from odoo import api, fields, models, _

class Picking(models.Model):
    _inherit = 'stock.picking'

    x_document_type = fields.Many2one('invoice.type',string='Tipo de comprobante de pago' , help='Document Number of the document related to the stock move. Invoice, External Move Document or internal move Document, in that order.')
    x_operation_type = fields.Many2one('stock.operation.type',string='Operation Type')