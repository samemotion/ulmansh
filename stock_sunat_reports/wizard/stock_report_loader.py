# -*- coding: utf-8 -*-
# Part of Same Motion. See LICENSE file for full copyright and licensing details.

#
# Order Point Method:
#    - Report Loader
#

from odoo import api, models, fields, _
import datetime
import calendar
from odoo.exceptions import ValidationError
#from odoo.tools import report

import logging
import threading

_logger = logging.getLogger(__name__)


class StockReportLoader(models.TransientModel):
    _name = 'stock.report.loader'
    _description = 'Stock Report Loader'
    
    x_month = fields.Selection([
            (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), 
            (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], \
            string='Month',  required=True)
    x_year = fields.Integer('Year', default= lambda self : str(int(datetime.datetime.now().year)),required=True)
    
    
    def create_report(self):
        #Search Records From Model

        report_name =  self.env.context.get('report_name',False)
        report_model = self.env.context.get('report_model',False)
        
        
#            report_model_obj = report_line_definition.x_model
#        else:
#            raise Warning ("No report definition for this report.")


#       date_field = report_line_definition.x_date_field.name
#        date_field_type = report_line_definition.x_date_field.ttype

#        if self.x_period_type == 'm':
        period_month = self.x_month
        period_year = self.x_year
        month_end_day = calendar.monthrange(int(period_year),int(period_month))[1]
        var_from_date = datetime.datetime.strptime(("%04d" % int(period_year)) + '-' +  ( "%02d" % int(period_month)) +  '-01','%Y-%m-%d')
        var_to_date = datetime.datetime.strptime(("%04d" % int(period_year)) + '-' +  ( "%02d" % int(period_month)) + '-' + ( "%02d" % month_end_day),'%Y-%m-%d')

        var_from_datetime = (var_from_date + datetime.timedelta(hours=5))
        var_to_datetime = (var_to_date + datetime.timedelta(hours=28, minutes=59, seconds=59))

            #Search Records From Model
#            if date_field:
#                if date_field_type == 'date':
#                    record_ids = self.env[report_model].search([[date_field, '>=', var_from_date], [date_field, '<=', var_to_date]])
#                elif date_field_type == 'datetime':
#                    record_ids = self.env[report_model].search([[date_field, '>=', str(var_from_datetime)], [date_field, '<=', #str(var_to_datetime)]])
#                else:
#                    raise Warning ( 'Date Field Type not valid. ')
#            else:
#                record_ids = self.env[report_model].search([], [])

#        elif self.x_period_type == 'y':
#            period_month = ''
#            period_year = self.x_year
#            var_from_date = datetime.datetime.strptime(("%04d" % int(period_year)) + '-01-01','%Y-%m-%d')
#            var_to_date = datetime.datetime.strptime(("%04d" % int(period_year)) + '-12-31','%Y-%m-%d')

#            var_from_datetime = (var_from_date + datetime.timedelta(hours=5))
#            var_to_datetime = (var_to_date + datetime.timedelta(hours=28, minutes=59, seconds=59))

            #Search Records From Model
#            if date_field:
#                if date_field_type == 'date':
        record_ids = self.env[report_model].search([])
#['date', '>=', var_from_date], ['date', '<=', var_to_date]
#                elif date_field_type == 'datetime':
#                    record_ids = self.env[report_model].search([[date_field, '>=', str(var_from_datetime)], [date_field, '<=', #str(var_to_datetime)]])
#                else:
#                    raise Warning ( 'Date Field Type not valid. ')
#            else:
#                record_ids = self.env[report_model].search([], [])

#        else:
#            record_ids = self.env[report_model].search([], [])

        #Filter by Company_id
#        ir_model_obj = self.env['ir.model.fields']
#        ir_model_field = ir_model_obj.search([('model_id','=',report_model_obj.id),('name','in',('company_id','x_company_id'))])
#        if len(ir_model_field)>0:
#            if ir_model_field[0].name == 'company_id':
#                record_ids = record_ids.filtered(lambda r: r.company_id.id == company_id.id)
#            elif ir_model_field[0].name == 'x_company_id':
#                record_ids = record_ids.filtered(lambda r: r.x_company_id.id == company_id.id)

        #Print Report
        context = self._context.copy()
        
        data =  self.env.context.get('active_id',False)
        datas = {
            
            'ids': record_ids.ids,
            'model': report_model,
            'form': data,
            'period_month': period_month,
            'period_year': period_year,
            'start_date': str(var_from_date),
            'end_date': str(var_to_date),
            'company_id': self.env['res.company']._company_default_get('stock.sunat.report').id,
            }
        
        
#        raise ValidationError(str(self.env['res.company']._company_default_get('stock.sunat.report').id))
#        if self.x_period_type in ('m','y'):
#         context.update({'period_month':period_month, 'period_year' : period_year,'start_date': str(var_from_date), 'end_date': str(var_to_date),'company_id':self.env['res.company']._company_default_get('stock.sunat.report').id })
#        elif self.x_period_type == 'd':
#            context.update({'x_to_date':self.x_to_date,'company_id':company_id.id,})
#        report_obj = self.env['report']
#        report = report_obj._get_report_from_name(report_name)
        
#        report = self.env['ir.actions.report']._get_report_from_name(report_name)
        #action = report.with_context(context).render_qweb_pdf(record_ids.ids)[0]
        #action = {'type': 'ir.actions.report.xml', 'report_name': report_name, 'datas': datas, 'context': context}
#        return report_obj.render('module.report_name', datas)

         
#        xml_ids = models.Model._get_external_ids(self.journal_id.x_report)
#        for model in self.journal_id.x_report:
#            module_names = set(xml_id.split('.')[0] for xml_id in xml_ids[model.id])
                        #model.modules = ", ".join(sorted(installed_names & module_names))
                        #raise Warning(str(xml_ids[model.id][0]))
#         raise ValidationError(report_name)

#         stock_report = self.env.ref(report_name)
#         return stock_report.with_context(context).report_action(self,data=data)
        return self.env.ref(report_name).with_context(context).report_action(self,data=datas)

#        attachment_file  = base64.b64encode(data)

        # self.x_txt_file = ""
        # random.seed()
        # num=str(random.randint(0,100))

#        self.write({
#            'x_txt_file_name':file_name + '.pdf',
#            'x_txt_file': attachment_file,
#        })
#        return {
#            'type': 'ir.actions.client',
#            'tag': 'reload',
#            }

class RegistroInventarioUnidades(models.AbstractModel):
    
    _name ='report.stock_sunat_reports.te_inventario_unidades'
        
    @api.model
    def get_report_values(self, docids, data=None):
        
        
        docs = []

        docs = self.env['stock.move'].search([
          ('date','<=',data['end_date']),
          ('state','=','done'),
          ('product_id.type','=','product'),
          ('product_id.location_id.usage','!=','transit')
        ])

        product_obj = docs.mapped('product_id')
        
        product_obj = product_obj.sorted(key=lambda r: r.name)
        
        warehouse_obj = docs.mapped('x_warehouse_id')

        #           <t t-set="product_obj" t-value="docs_filtered.mapped('product_id')"/>
        #                   <t t-set="warehouse_obj" t-value="docs_filtered.mapped('x_warehouse_id')"/>
        #         docs = self.env[data['model']].search([])
        #         raise ValidationError(docs)
        
        #raise ValidationError(var_from_date)
        
        docs = docs.filtered( lambda r: (r.date > data['start_date']) and (r.date < data['end_date'] ) and r.state == 'done')
        docs = docs.sorted(lambda r: r.date)
        
#         raise ValidationError("Testing")
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'period_month': data['period_month'],
            'period_year': data['period_year'],
            'company_id': data['company_id'],
            'docs' : docs,
            'product_obj': product_obj,
            'warehouse_obj': warehouse_obj,
            'prueba': "Probando datos"
         }