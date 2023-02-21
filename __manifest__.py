# -*- coding: utf-8 -*-
{
    'name': "bar_app",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups_bar_security.xml',
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/ingredient_view.xml',
        'views/category_view.xml',
        'views/table_view.xml',
        'views/invoice_view.xml',
        'views/order_view.xml',
        'views/menu.xml',
        'reports/report.xml',
        
        'reports/order_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application':True,
    'installable':True,
}
