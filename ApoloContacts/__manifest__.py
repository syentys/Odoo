# -*- coding: utf-8 -*-
{
   'name' : "ApoloContacts",
   'version' : "1.0",
   'author' : "SYENTYS",
   'website': 'http://www.syentys.com',
   'description': """
       Date de dernière mise à jour: 27/02/2018 
       
       Module de personalisation des contacts selon cahier des charges APOL
    """,
   'depends' : ['contacts', 'crm', 'sale', 'sale_margin', 'purchase', 'point_of_sale'],
   'data' : [
        'data/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',
        'views/ApoloContacts_view.xml',
        'views/geo_view.xml',
        'views/purchase_order_view.xml',
        'views/kanban_view.xml',
        'views/templates.xml'
   ],
   'installable' : True,
}
