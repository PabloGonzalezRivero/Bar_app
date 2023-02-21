import datetime
from odoo import models, fields, api


class InvoiceModel(models.Model):
        _name = 'bar_app.invoice_model'
        _description = 'This is the invoice model'
        _sql_constraints = [ ('bar_app_ref_uniq','UNIQUE (ref)','There cannot be two invoices with the same ref')]

        ref = fields.Integer(string="Ref",help="Invoice's ref",required=True,index=True,default=lambda self: self.setRef() ,readonly=1) #Must be autoincrementable
        date = fields.Datetime(string="Generation Date",required=True, default=lambda self:datetime.datetime.now())
        base = fields.Float(string="base cost",compute='_setPrice',help="Cost without VAT")
        VAT = fields.Selection(string="VAT",selection=[("0",0.0),("4",4.0),("10",10.0),("21",21.0)], default="0")
        tcost = fields.Float(string="Total cost",compute='setTotalPrice',help="Bill of the table" ,readonly=1 , store=True)
        currency_id= fields.Many2one('res.currency',string="Currency", default=lambda self:self.env.user.company_id.currency_id)
        products = fields.One2many('bar_app.order_model',inverse_name="numref",string="lineOrders",help="Lines of orders")
        state = fields.Selection(string="Status of the invoice",selection=[('D','Draft'),('C','Confirmed')], default="D")
        client = fields.Text(string="Client",help="Indication of the clients")




        def setRef (self):
                listref = self.env["bar_app.invoice_model"].sudo().search([])
                if len(listref) ==0:
                        return 1
                else:
                        return (listref[-1]["ref"]+1)


        @api.depends("products")
        def _setPrice(self):
                for rec in self:
                        rec.base=0
                        for prod in rec.products:
                                rec.base +=  prod.price


        @api.depends("base")
        def setTotalPrice(self):
                for rec in self:
                        rec.tcost=0
                        if  rec.VAT == 0.0:
                                rec.tcost = rec.base
                        else:        
                                rec.tcost = (rec.base + ((rec.base * int(rec.VAT)) / 100))

        def changeStateToDraft(self):
                self.state = "D"  
        
        def changeStateToConfirmed(self):
                self.state = "C"
