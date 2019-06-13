
from odoo import api, models, fields, _
import datetime
import calendar
from odoo.exceptions import ValidationError
from odoo.http import request


import threading
import base64
from itertools import zip_longest

from PyPDF2 import PdfFileMerger
import gc
import io

import logging
_logger = logging.getLogger(__name__)


class StockReportLoader(models.TransientModel):
    _name = 'stock.report.loader'
    _description = 'Stock Report Loader'

    x_month = fields.Selection([
            (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
            (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], \
            string='Month',  required=True)
    x_year = fields.Integer(
        'Year',
        default= lambda self : str(int(datetime.datetime.now().year)),
        required=True)

    x_attachments_ids = fields.Many2many('ir.attachment', string="Attachments")

    @staticmethod
    def grouper(iterable, n, fillvalue=None):
        args = [iter(iterable)] * n
        return zip_longest(*args, fillvalue=fillvalue)

    @api.multi
    def generate_multi_pdf(self, report_name, values, context):

        report = self.env['ir.actions.report']._get_report_from_name(
            'stock_sunat_reports.te_inventario_unidades'
        )

        report_model_name = 'report.%s' % ('stock_sunat_reports.te_inventario_unidades')
        report_model = self.env.get(report_model_name)

        if report_model is not None:

            data = report_model.get_report_values(values['ids'], data=values)
            
#         raise ValidationError(data['product_obj'])

        _logger.info("Esta es la data que se renderiza en el reporte")
        _logger.info(data)
        
        html = report.render_template('stock_sunat_reports.te_inventario_unidades', values=data)
        
        html = html.decode('utf-8')

        bodies, html_ids, header, footer, specific_paperformat_args = report.with_context(context)._prepare_html(html)
        
        
        pdf_content = report._run_wkhtmltopdf(
            bodies,
            header=header,
            footer=footer,
            landscape=context.get('landscape'),
            specific_paperformat_args=specific_paperformat_args,
            set_viewport_size=context.get('set_viewport_size'),
        )

        return pdf_content
#         return base64.encodestring(pdf_content)

    @api.multi
    def create_report(self):

        report_name = self.env.context.get('report_name',False)
        report_model = self.env.context.get('report_model',False)

        period_month = self.x_month
        period_year = self.x_year
        month_end_day = calendar.monthrange(int(period_year),int(period_month))[1]
        var_from_date = datetime.datetime.strptime(("%04d" % int(period_year)) + '-' +  ( "%02d" % int(period_month)) +  '-01','%Y-%m-%d')
        var_to_date = datetime.datetime.strptime(
            ("%04d" % int(period_year)) + '-' +  ( "%02d" % int(period_month)) + '-' + ( "%02d" % month_end_day),'%Y-%m-%d')
        var_from_datetime = (var_from_date + datetime.timedelta(hours=5))
        var_to_datetime = (var_to_date + datetime.timedelta(hours=28, minutes=59, seconds=59))
        
        
        # var_to_date is the original implementation
        record_ids = self.env[report_model].search([
          ('date', '<=', str(var_to_date)),
          ('state', '=', 'done'),
          ('product_id.type', '=', 'product'),
          ('product_id.location_id.usage', '!=', 'transit')
        ])
        
        
        
        ## Check this logic when filtering records 
        product_obj = record_ids.mapped('product_id')
        
        
        product_obj_filtered = product_obj.filtered(
            lambda r: r.with_context(
                to_date=str(var_from_date)
                ).qty_at_date != 0 and r.active is True ) 

        record_ids = record_ids.filtered(
            lambda r: (r.date > str(var_from_date)) and
            (r.date < str(var_to_date)) and
            (r.state == 'done') and
            (r.product_id.type == 'product') and
            (r.product_id.location_id.usage != 'transit'))
        
        ##################

        record_ids = record_ids.sorted(lambda r: r.date)
        
        
        
        # Here setup dict datato use on report
        origins = [str(p.picking_id.origin) for p in record_ids if (p.picking_id.origin is not False and p.picking_id.origin is not '')]
#         raise ValidationError(origins)
#         raise ValidationError(len(origins))
#         raise ValidationError("test")
        
        invoices = self.env['account.invoice'].search([('origin','in',origins)])
#         raise ValidationError(invoices)
        
        origin_data = {}
        for inv in invoices:
            
            origin_data[str(inv.origin)] = {
                
                'serial': inv.x_document_serial,
                'number': inv.x_document_correlative,
                'type': inv.journal_id.x_document_type.x_code,
                'operation_type': "01",
            }
        #Generally speaking we could have this
        

        product_obj_filtered2 = record_ids.mapped('product_id')
        

        product_obj = product_obj_filtered | product_obj_filtered2

        # f2 = len(product_obj_filtered2)
        # t  = len(product_obj)
        # size = "f1: %s, f2: %s, t: %s" %( str(f1),str(f2),str(t))

        product_obj = product_obj.sorted(key=lambda r: r.name)
        
        docs_ids = [str(d.id) for d in record_ids]

        move_lines = self.env['stock.move.line'].search(
            [('move_id.id', 'in', docs_ids)]
        )

        context = self._context.copy()

        data = self.env.context.get('active_id', False)

        product_iterator = self.grouper(product_obj, 500)

        pdf_streams = []
        streams = []
        stream_ids = []
        
        pdf_merger = PdfFileMerger()
#         for stream in streams:
#                 pdf_merger.append(stream)

#         with open(output_path, 'wb') as fileobj:
#             pdf_merger.write(fileobj)

        Attachment = self.env['ir.attachment']

        for product in product_iterator:

            datas = {

                'ids': record_ids.ids,
                'model': report_model,
                'form': data,
                'period_month': period_month,
                'period_year': period_year,
                'start_date': str(var_from_date),
                'end_date': str(var_to_date),
                'company_id': self.env['res.company']._company_default_get('stock.sunat.report').id,
                'product_obj': product,
                'docs': record_ids,
                'move_lines': move_lines,
                'origin_data': origin_data,
                }
            
            
#             _logger.info("Datos que se pasan a la funcion del pdf")
#             _logger.info(datas)

            pdf = self.with_context(context).generate_multi_pdf(
                'stock_sunat_reports.te_inventario_unidades',
                values=datas,
                context=context
            )
            
            pdf_streams.append(pdf)
            
            _logger.info(pdf_streams)
            
#         raise ValidationError("test")
        del product_obj
        del record_ids
        del move_lines
        del datas
        del product_obj_filtered2
        del product_obj_filtered
        
        gc.collect() # to free all memory used until now
        
        #test
        
        file_io= io.BytesIO(pdf)
        
        for pdf in pdf_streams:
            
            pdf_merger.append(io.BytesIO(pdf))
        
#         file_handlers = []
        
#         for i, pdf in enumerate(pdf_streams):
            
#             file_handlers.append(open(str(i)+'.pdf',"wb+"))

#             file_handlers[i].write(pdf)
#             pdf_merger.append(fileobj=file_handlers[i])
            
        myio = io.BytesIO()
        pdf_merger.write(myio)
        pdf_merger.close()
        
#         for f in file_handlers:
#             f.close()
        
        myio.seek(0)
        myio.read()
        
#         string_bytes = io.StringIO()
        string_bytes = myio.getvalue()

        # Here works but need merge the pdf files
        
            
#         for pdf in pdf_streams:
            
#             data_attach = {
#                 'name': "TT3.pdf",
#                 'datas': pdf,
#                 'datas_fname': "TT3.pdf",
#                 'res_model': 'stock.report.loader',
#                 'res_id': 0,
#                 'mimetype':'application/pdf',
#                 'type': 'binary',  # override default_type from context, possibly meant for another model!
#             }
        
#             streams.append(Attachment.create(data_attach))
            
            
#             f = open("Test", 'wb+')
#             f.write(pdf)
#             pdf_merger.append(fileobj=f)
#             pdf_merger.append(fileobj=f)
#             f.close()
            
#             del pdf
#             del datas
#             del f
#             gc.collect()
            
#         myio = io.BytesIO()
#         pdf_merger.write(myio)
#         pdf_merger.close()
        
        
#         myio.seek(0)
#         myio.read()
        
#         string_bytes = io.StringIO()
#         string_bytes = myio.getvalue()
        
#         raise ValidationError(test)
        
#         with open('Testing.pdf', 'wb') as fileobj:
#             ff = pdf_merger.write(fileobj)
        
        Attachment = self.env['ir.attachment']

        data_attach = {
            'name': "TT3.pdf",
            'datas': base64.encodestring(string_bytes),
            'datas_fname': "TT3.pdf",
            'res_model': 'stock.report.loader',
            'res_id': 0,
            'mimetype':'application/pdf',
            'type': 'binary',  # override default_type from context, possibly meant for another model!
        }


# #         Esto es importante
#         stream_ids = [ s.id for s in streams]       
#         self.x_attachments_ids = stream_ids
        self.x_attachments_ids = [Attachment.create(data_attach).id]


        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.report.loader',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        
        
#         return {
#             'context': context,
#             'data': data,
#             'type': 'ir.actions.report',
#             'report_name': 'stock_sunat_reports.te_inventario_unidades',
#             'report_type': 'qweb-pdf',
#             'report_file': ff,
#             'name': "Testing PDF",
#         }


class RegistroInventarioUnidades(models.AbstractModel):

    _name = 'report.stock_sunat_reports.te_inventario_unidades'

    @api.model
    def get_report_values(self, docids, data=None):

        warehouse_obj = data['docs'].mapped('x_warehouse_id')
        
#         keys = ""
#         for d in data['origin_data']:
            
#             keys += " key : %s, otros: %s %s \n" % (d,data['origin_data'][d]['type'],data['origin_data'][d]['serial'])
            
#         raise ValidationError(keys)
        
        complete_dict = {}
        
        # Is a trick to use filtered to get my records easier but maybe i have to do it manually decide based on performance
        products = self.env['product.product']
        
        for p in data['product_obj']:
            
            if p != None:
                products |= p
    
        data['product_obj'] = products
        
        moves_by_product_and_warehouse = {}
        
        for warehouse in warehouse_obj:
            
            for product in data['product_obj']:
                
                if product is None:
                    
                    continue
                       
                #docs_product_obj_ordered = data['docs'].filtered( lambda r: r.product_id.id == product.id)
                
                moves_by_product_and_warehouse[str(product.id)+str(warehouse.id)] = data['move_lines'].filtered(lambda r: r.product_id.id == product.id and r.x_warehouse_id.id == warehouse.id)
            
        
#         for product in data['product_obj']:
            
#             if product is None:
#                 continue
            
#             docs_product_obj_ordered = data['docs'].filtered( lambda r: r.product_id.id == product.id)
            
#             complete_dict[product.id] = {

#                 'records': docs_product_obj_ordered,
#                 'total_incoming': sum(
#                     line.quantity_done for line in docs_product_obj_ordered.filtered(lambda r: r.picking_code != 'incoming')
#                 ),
#                 'total_outgoing': sum(
#                     line.quantity_done for line in docs_product_obj_ordered.filtered(lambda r: r.picking_code == 'outgoing')
#                 ),

#             }
                    
#         _logger.info("Datos de origin data")
#         _logger.info(data['origin_data'])
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'period_month': data['period_month'],
            'period_year': data['period_year'],
            'company_id': data['company_id'],
            'docs': data['docs'],
            'product_obj': data['product_obj'],
            'warehouse_obj': warehouse_obj,
            'all_move_lines': data['move_lines'],
            'moves_by_product_and_warehouse': moves_by_product_and_warehouse,
            'origin_data': data['origin_data'],

         }
