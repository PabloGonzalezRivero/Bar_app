from odoo import models, fields,api
from odoo.exceptions import ValidationError


class ProductModel(models.Model):
        _name = 'bar_app.product_model'
        _description = 'This is the product model'

        id = fields.Integer(string="ID",help="Product's id",required=True,index=True)
        name = fields.Text(string="Product's name",help="Name of the product",required=True)
        description = fields.Text(string="Product's description",help="Description of the product")
        image = fields.Image(string="Image")
        category = fields.Many2many('bar_app.category_model',string="Category")
        ingredients = fields.Many2many('bar_app.ingredient_model',string="Ingredients")
        price = fields.Monetary(string="Price")
        currency_id= fields.Many2one('res.currency',string="Currency", default=lambda self:self.env.user.company_id.currency_id)
        #Añadir una serie de observaciones segun que tipo de producto sea



        @api.constrains("price")
        def _checkPrice(self):
                if (self.price) <=0:
                        raise ValidationError("The price can't be lesser than 0")