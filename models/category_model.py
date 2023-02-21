from odoo import models, fields, api


class CategoryModel(models.Model):
        _name = 'bar_app.category_model'
        _description = 'This is the category model'
        _rec_name = 'complete_name'
        _order = 'complete_name'

        id = fields.Integer(string="ID",help="Category's id",required=True,index=True)
        name = fields.Text(string="Category's name",help="Name of the category",required=True)
        complete_name = fields.Char('Complete Name',compute='_compute_complete_name',recursive=True,store=True)
        description = fields.Text(string="Category's description",help="Description of the category")
        products = fields.Many2many('bar_app.product_model',inverse_name="category",string="Products",help="List of products of this category")
        parent_id = fields.Many2one('bar_app.category_model',string="Parent Category",index=True,ondelete="cascade")
        child_ids = fields.One2many('bar_app.category_model',"parent_id",string="Child categories")


        
        @api.depends('name','parent_id.complete_name')
        def _compute_complete_name(self):
                for category in self:
                        if category.parent_id:
                                category.complete_name = '%s/%s' % (category.parent_id.complete_name, category.name)
                        else:
                                category.complete_name = category.name
        