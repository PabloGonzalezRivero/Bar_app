from odoo import models, fields,api


class OrderModel(models.Model):
        _name = 'bar_app.order_model'
        _description = 'This is the order model'
        

        id = fields.Integer(string="ID",help="Order's id",required=True,index=True)
        Table = fields.Many2one('bar_app.table_model',string="Product")
        numref = fields.Many2one('bar_app.invoice_model',string="Product")
        numTable =fields.Integer(default=lambda self: self.setNum() ,readonly=1)
        product = fields.Many2one('bar_app.product_model',inverse_name="category",string="Product",help="The product of the lineorder",required=True)
        quantity = fields.Integer(string="Quantity",help="Quantity of the product",default=1, required=True)
        price = fields.Monetary(string="Price")
        done = fields.Boolean(string="Is the product done",default=False)
        delivered = fields.Boolean(string="Is the product delivered",default=False)
        getFrom = fields.Selection(string="Make it in the kitchen or take it from the bar",selection=[('K','Kitchen'),('B','Bar')], default="K")
        currency_id= fields.Many2one('res.currency',string="Currency", default=lambda self:self.env.user.company_id.currency_id)
        #Añadir una serie de observaciones segun que tipo de producto sea

        #Observaciones no controladas por la selección.
        observation = fields.Text(string="Information about the ingredient")


        def setRef (self):
                for rec in self:
                        return rec.Table.num

        @api.onchange("product","price","quantity")
        def setPrice(self):
            #Sacar el precio del producto para multiplicarlo por la cantidad del producto
            for rec in self:
                rec.price = rec.quantity * rec.product.price

        def changeStateToDoneKitchen(self):
                self.done = True
                return { 
                'name': ('Order List Kitchen'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'bar_app.order_model',
                'domain': [('getFrom','=','K'),('done','=',False)],
                'view_id': False,
                'views': [(self.env.ref('bar_app.order_model_tree_bar').id, 'tree'),(self.env.ref('bar_app.order_model_form_bar').id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'current',
                }

        
        def changeStateToDoneBar(self):
                self.done = True
                return { 
                'name': ('Order List Bar'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'bar_app.order_model',
                'domain': [('getFrom','=','B'),('done','=',False)],
                'view_id': False,
                'views':[(self.env.ref('bar_app.order_model_tree_bar').id, 'tree'),(self.env.ref('bar_app.order_model_form_bar').id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'current',

                }

        def changeStateToDelivered(self):
                self.delivered = True
                return { 
                'name': ('Order List Waiter'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'bar_app.order_model',
                'domain': [('done','=',True),('delivered','=',False)],
                'view_id': False,
                'views': [(self.env.ref('bar_app.order_model_tree_waiter').id, 'tree'),(self.env.ref('bar_app.order_model_form_waiter').id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'current',
   
                }