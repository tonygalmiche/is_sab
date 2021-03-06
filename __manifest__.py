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
        'event_sale',
        'association',
        'membership',
    ],
    'data' : [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'wizard/is_event_recurrent_wizard_view.xml',
        'views/event_views.xml',
        'views/is_groupe_views.xml',
        'views/is_materiel_views.xml',
        'views/is_livre_views.xml',
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
        'static/src/xml/web_kanban_activity.xml',
    ],

}

