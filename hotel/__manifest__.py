# -*- coding: utf-8 -*-
{
    'name': "hotel",
    'summary': "Hotel Management System",
    'description': "Hotel Guest Registration and Billing System",
    'author': "ROYTEK",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in module listings
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hotel',
    'version': '18.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    
    'application': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mainMenu.xml',
        'views/charges.xml',
        'views/roomTypes.xml',
        'views/rooms.xml',
        'views/guests.xml',
        'views/guestregistration.xml',
        # 'views/hoteldocuments.xml',
    ],
    
    '''
    'assets': {
        'web.assets_backend': [
            'hotel/static/src/css/custom.css',
        ],
    },

    'images': ['static/description/icon.png'],
    '''

    'installable': True,
    'application': True,
}