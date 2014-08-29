# -*- encoding: utf-8 -*-
################################################################################
#    See Copyright and Licence Informations undermentioned.
################################################################################

#TODO: 
#offer more options to calculate the average consumption

{
    'name': 'Computed Purchase Order',
    'version': '2.2',
    'category': 'Purchase',
    'description': """
Provide tools to help purchaser during purchase process
=======================================================

Functionnality :
----------------
    This module helps you to decide what you have to buy.
    1) Create a new Compute Purchase Order (CPO)
    2) Select a Supplier
    3) Check the boxes to tell if you want to take into account the virtual stock or the draft sales/purchases
    4) Use the button to import the list of products you can purchase to this supplier (ie: products that have a product_supplierinfo for this partner). It especially calculates for each product:
        - the quantity you have or will have;
        - the average_consumption, based on the stock moves created during last 365days;
        - the theorical duration of the stock, based on the precedent figures.
    5a) Unlink the products you don't want to buy anymore to this supplier (this only deletes the product_supplierinfo)
    5b) Add new products you want to buy and link them (this creates a product_supplierinfo)
    5c) Modify any information about the products: supplier product_code, supplier product_name, purchase price, package quantity, purchase UoM.
    5d) Modify the calculated consumption if you think you'll sell more or less in the future.
    5e) Add a manual stock quantity (positive if you will receive products that are not registered at all in OE, negative if you have not registered sales)
    6) Click the "Update Products" button to register the changes you've made into the product supplierinfo.
    7) Check the Purchase Target. It's defined on the Partner form, but you still can change it on each CPO.
    8) Click the button to calculate the quantities you should purchase. It will compute a purchase order fitting the purchase objective you set, trying to optimize the stock duration of all products.
    9) Click the "Make Order" button to convert the calculation into a real purchase order.

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author : 
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'product_average_consumption',
        'purchase',
        'purchase_package_qty',
    ],
    'data': [
        'data/function.xml',
        'data/ir_sequence.xml',
        'security/ir_rule_data.yml',
        'security/ir_model_access_data.yml',
        'view/update_product_wizard_view.xml',
        'view/action.xml',
        'view/view.xml',
        'view/menu.xml',
        ],
    'demo': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'application' : True,
    'installable': True,
    'auto_install': False,
}
