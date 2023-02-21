from odoo import models, fields


class IngredientModel(models.Model):
        _name = 'bar_app.ingredient_model'
        _description = 'This is the ingredien model'

        id = fields.Integer(string="ID",help="Ingredient's id",required=True,index=True)
        name = fields.Text(string="Ingredient's name",help="Name of the ingredient",required=True)
        observation = fields.Text(string="Information about the ingredient")
        products = fields.Many2many('bar_app.product_model',string="Products")

        
