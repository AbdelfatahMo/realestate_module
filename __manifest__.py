# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        Manage real estate agences works """,

    'description': """
        Save and easy reach to estates and save offers from clients.
        Save all details about estates and their description.
    """,

    'author': "Abdelfatah Mohamad",
    'website': "abdelfatah.mohamad.99@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Management',
    'version': '16.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    "application":True,
    "installable":True,
    "auto_install":False,
}
