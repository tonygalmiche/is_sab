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
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/event_views.xml',
        'views/is_groupe_views.xml',
        'views/is_materiel_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
    ],
}

