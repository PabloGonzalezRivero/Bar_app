from odoo import models, fields,api
from odoo.exceptions import ValidationError
import requests
 

class TableModel(models.Model):
        _name = 'bar_app.table_model'
        _description = 'This is the table order model'
        #Hacer el constraint por metodo

        #Pensar en cambiar el identificador numtable por un id
        num = fields.Integer(string="Num",help="Number of the table",required=True,index=True)
        pax = fields.Integer(string="Pax",help="Number of clients of the table",default=1)
        active = fields.Boolean(string="Is the order",help="The order is active?",default=True)
        client = fields.Text(string="Client",help="Indication of the clients" )
        waiter = fields.Text(string="Waiter",help="The waiter who assisted the table" ,default = lambda self: self.env.user.name)
        tcost = fields.Float(string="Total cost",compute='_setPrice',help="Bill of the table" ,readonly=1 ,store=True)
        currency_id= fields.Many2one('res.currency',string="Currency", default=lambda self:self.env.user.company_id.currency_id)
        lineOrders = fields.One2many('bar_app.order_model',inverse_name="numTable",string="lineOrders",help="Lines of orders")
        state = fields.Selection(string="Status of the order",selection=[('O','Order in progress'),('D','Draft'),('C','Confirmed')], default="O")
        #invoice = fields.Many2one("bar_app.invoice_model",string = "Invoice", compute="_generateInvoice",store=True,recursive=True)
        ordersdone = fields.Boolean(string="Are all the orders done?",default=False)

        @api.constrains("num")
        def _constraintNum(self):
                tables=self.search([("active","=",True)])
                for table in tables:
                        if self.num==table.num and self.id != table.id:
                                raise ValidationError("A table with the same number is already active")
                        

        @api.depends("lineOrders.done","lineOrders.price","lineOrders.delivered")
        def _setPrice(self):
                for rec in self:
                        rec.tcost=0
                        for line in rec.lineOrders:
                                if line.delivered==True:
                                        rec.ordersdone=True
                                else:
                                        rec.ordersdone=False
                                        break
                        for reco in rec.lineOrders:
                                rec.tcost += reco.price

       
                        



        """""
        @api.constrains("num","state")
        def _checkTable(self):
                if len(self.taskname) <5:
                        raise ValidationError("The  name must have mor than five characters")
        """
        

        def changeStateToInProgress(self):
                self.state = "O"  

        def changeStateToDraft(self):
                self.state = "D"

        #Trigger new invoice when the table is confirmed
        def changeStateToConfirm(self):

                if self.ordersdone==True:
                         self.state = "C"    
                         invoice={}
                         invoice["products"] = self.lineOrders
                         invoice["client"] = self.client
                         response = invoice
                         self.env["bar_app.invoice_model"].sudo().create(response)
                         self.active = False
                else:
                        raise ValidationError("There are orders that aren't confirmed")

        #self.env.user.name
        @api.onchange("num")
        def numTable(self):
                self.client= "Table "+str(self.num)

        
        

        