# -*- coding: utf-8 -*-
{
    'name'     : 'InfoSaône - Module Odoo 12 pour SAB',
    'version'  : '0.1',
    'author'   : 'InfoSaône',
    'category' : 'InfoSaône',
    'description': """
InfoSaône - Module Odoo 12 pour SAB
===================================================
""",
    'maintainer' : 'InfoSaône',
    'website'    : 'http://www.infosaone.com',
    'depends'    : [
        'base',
        'sale',
        'sale_management',
        'document',
        'product',
        'purchase',
        'event',
        'association',
        'membership',
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/event_views.xml',
        #'views/res_partner_views.xml',
        #'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
    ],
}

