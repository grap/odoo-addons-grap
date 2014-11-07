# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Move Change Number Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Account - Move Change Number',
    'version': '1.0',
    'category': 'Accounting',
    'description': """
Allow special user to rename account move
=========================================

Features :
----------
    * Allow special user to rename account move ;
      Usefull if the account move doesn't have the good numeration.
      (for exemple if you change account move sequence) ;

Technical informations :
------------------------
    * change account move name with next sequence ;
    * add in the field 'narration' the old name ;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'security/res_groups_data.yml',
        'view/view.xml',
        'view/action.xml',
    ],
}
