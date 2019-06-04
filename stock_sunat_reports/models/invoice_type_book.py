from odoo import models, fields,api

class InvoiceType(models.Model):
    _name = 'invoice.type.book'

    x_name = fields.Char(string = 'Name')
    x_code = fields.Char(string  = 'Code')
    x_visible_in_module = fields.Selection([('purchase','Purchase'),('sale','Sale'),('invoice','Invoice'),('general','General'),('all','All')],string="Visible in Module",help="Module where the invoice type could be found")
    x_document_serial_min_characters = fields.Integer('Document Serial Minimum Characters')
    x_document_serial_max_characters = fields.Integer('Document Serial Maximum Characters')
    x_document_serial_data_validation = fields.Char(string='Document Serial Data Validation',help="Python validation")
    x_document_serial_validation_message = fields.Char(string='Document Serial Validation Message',translate=True)
    x_document_correlative_min_characters = fields.Integer('Document Correlative Minimum Characters')
    x_document_correlative_max_characters = fields.Integer('Document Correlative Maximum Characters')
    x_document_correlative_data_validation = fields.Char(string='Document Correlative Data Validation',help="Python validation")
    x_document_correlative_validation_message = fields.Char(string='Document Correlative Validation Message',translate=True)
