odoo.define('pos_inv_ticket.screens', function (require) {
    "use strict";
    var screen = require('point_of_sale.screens');
    var field_utils = require('web.field_utils');
    // var QWeb = core.qweb;
    var rpc = require('web.rpc');

    screen.PaymentScreenWidget = screen.PaymentScreenWidget.include({
        finalize_validation: function() {
            var self = this;
            var order = this.pos.get_order();
    
            if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) { 
    
                    this.pos.proxy.open_cashbox();
            }
    
            order.initialize_validation_date();
            order.finalized = true;

            if (order.is_to_invoice()) {
                var invoiced = this.pos.push_and_invoice_order(order);
                this.invoicing = true;
    
                invoiced.fail(function(error){
                    self.invoicing = false;
                    order.finalized = false;
                    if (error.message === 'Missing Customer') {
                        self.gui.show_popup('confirm',{
                            'title': _t('Please select the Customer'),
                            'body': _t('You need to select the customer before you can invoice an order.'),
                            confirm: function(){
                                self.gui.show_screen('clientlist');
                            },
                        });
                    } else if (error.code < 0) {        // XmlHttpRequest Errors
                        self.gui.show_popup('error',{
                            'title': _t('The order could not be sent'),
                            'body': _t('Check your internet connection and try again.'),
                        });
                    } else if (error.code === 200) {    // OpenERP Server Errors
                        self.gui.show_popup('error-traceback',{
                            'title': error.data.message || _t("Server Error"),
                            'body': error.data.debug || _t('The server encountered an error while receiving your order.'),
                        });
                    } else {                            // ???
                        self.gui.show_popup('error',{
                            'title': _t("Unknown Error"),
                            'body':  _t("The order could not be sent to the server due to an unknown error"),
                        });
                    }
                });
    
                invoiced.done(function(){
                    self.invoicing = false;
                    // self.gui.show_screen('receipt');

                    rpc.query({
                        model: 'pos.order',
                        method: 'get_invoice_info',
                        args: [[], [order.name]],
                    })
                    .then(function (res) {
                        // console.log('after =', new Date());
                        // console.log(res);
                        order.info = res
                        console.log(order);
                        self.gui.show_screen('receipt');
                    });
                });
            } else if (order.is_to_ticket()) {
                var invoiced = this.pos.push_and_invoice_order(order);
                this.invoicing = true;
    
                invoiced.fail(function(error){
                    self.invoicing = false;
                    order.finalized = false;
                    if (error.message === 'Missing Customer') {
                        self.gui.show_popup('confirm',{
                            'title': _t('Please select the Customer'),
                            'body': _t('You need to select the customer before you can invoice an order.'),
                            confirm: function(){
                                self.gui.show_screen('clientlist');
                            },
                        });
                    } else if (error.code < 0) {        // XmlHttpRequest Errors
                        self.gui.show_popup('error',{
                            'title': _t('The order could not be sent'),
                            'body': _t('Check your internet connection and try again.'),
                        });
                    } else if (error.code === 200) {    // OpenERP Server Errors
                        self.gui.show_popup('error-traceback',{
                            'title': error.data.message || _t("Server Error"),
                            'body': error.data.debug || _t('The server encountered an error while receiving your order.'),
                        });
                    } else {                            // ???
                        self.gui.show_popup('error',{
                            'title': _t("Unknown Error"),
                            'body':  _t("The order could not be sent to the server due to an unknown error"),
                        });
                    }
                });
    
                invoiced.done(function(){
                    self.invoicing = false;
                    // self.gui.show_screen('receipt');
                    rpc.query({
                        model: 'pos.order',
                        method: 'get_invoice_info',
                        args: [[], [order.name]],
                    })
                    .then(function (res) {
                        // console.log('after =', new Date());
                        // console.log(res);
                        order.info = res
                        console.log(order);
                        self.gui.show_screen('receipt');
                    });
                });
            } else {    
                this.pos.push_order(order);
                this.gui.show_screen('receipt');
            }
        },
    });

    screen.ReceiptScreenWidget = screen.ReceiptScreenWidget.include({
        show: function(){
            this._super();
            var self = this;
    
            this.render_change();
            this.render_receipt();
            this.render_receipt_lines();
            this.handle_auto_print();
        },
        render_receipt_lines: function() {
            // this.$('.pos-receipt-container').html(QWeb.render('PosTicket', this.get_receipt_render_env()));
            let order = this.pos.get_order();
            let cashier = this.pos.get_cashier();
            console.log('render_receipt_lines!!!!');
            console.log(order);
            
            this.$('.business').text(order.info.business_name);
            this.$('.street').text(order.info.street);

            let html = this.$('.invoice-line').html();
            if(!html) return;
            html = '<div class="invoice-line">'+ html +'</div>';
            
            //invoice lines
            for(let line of order.info.lines){
                html += '<div class="invoice-line">';
                html += '   <div class="paragraph small">'+ line.quantity +'</div>';
                html += '   <div class="paragraph large">'+ line.description +'</div>';
                html += '   <div class="paragraph medium">'+ order.info.currency_symbol + ' ' + line.price_unit.toFixed(2) +'</div>';
                html += '   <div class="paragraph medium">'+ order.info.currency_symbol + ' ' + line.subtotal.toFixed(2) +'</div>';
                html += '</div>';
            }

            html += '<br/>';
            html += '<div class="invoice-total">';
            html += '   <div class="paragraph small"></div>';
            html += '   <div class="paragraph large"></div>';
            html += '   <div class="paragraph medium">Total</div>';
            html += '   <div class="paragraph medium">'+ order.info.currency_symbol + ' ' + order.get_total_with_tax().toFixed(2) +'</div>';
            html += '</div>';

            html += '<div class="invoice-total">';
            html += '   <div class="paragraph small"></div>';
            html += '   <div class="paragraph large"></div>';
            html += '   <div class="paragraph medium">Op. Gravada</div>';
            html += '   <div class="paragraph medium">'+ order.info.currency_symbol + ' ' + order.get_total_without_tax().toFixed(2) +'</div>';
            html += '</div>';

            for (let taxdetail of order.get_tax_details()){
                html += '<div class="invoice-total">';
                html += '   <div class="paragraph small"></div>';
                html += '   <div class="paragraph large"></div>';
                html += '   <div class="paragraph medium">'+ taxdetail.name +'</div>';
                html += '   <div class="paragraph medium">'+ order.info.currency_symbol + ' ' + taxdetail.amount.toFixed(2) +'</div>';
                html += '</div>';
            }

            html += '<br/>'
            for (let line of order.paymentlines.models){
                html += '<div class="invoice-total">';
                html += '   <div class="paragraph xxlarge"></div>';
                html += '   <div class="paragraph large"></div>';
                html += '   <div class="paragraph medium">'+ line.name +'</div>';
                html += '   <div class="paragraph medium">'+ order.info.currency_symbol + ' ' + line.amount.toFixed(2) +'</div>';
                html += '</div>';
            }

            html += '<div class="invoice-total">';
            html += '   <div class="paragraph xxlarge"></div>';
            html += '   <div class="paragraph large"></div>';
            html += '   <div class="paragraph medium">Vuelto</div>';
            html += '   <div class="paragraph medium">'+ order.info.currency_symbol + ' ' + order.get_change().toFixed(2) +'</div>';
            html += '</div>';

            this.$('.invoice-line').replaceWith(html);
            

            html = this.$('.qr-code').html();
            console.log('.qr-code');
            console.log(html);
            if(!html) return;
            
            html = '<div class="qr-code">'+ html +'</div>';

            html += '<br/>';
            html += '<div class="invoice-detail">';
            
            if(order.is_to_invoice())
                html += '<div class="paragraph">Representación impresa de la Factura Electrónica</div>';
            else
                html += '<div class="paragraph">Representación impresa de la Boleta Electrónica</div>';

            html += '   <div class="paragraph">Consulte su comprobante de pago en:</div>';
            html += '   <div class="paragraph">'+ order.info.qr_link +'</div>';
            html += '</div>';
        

            this.$('.qr-code').replaceWith(html);
        }
    });

});