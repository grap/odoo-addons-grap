# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change eMail module for Odoo
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
    'name': 'GRAP - Change eMail',
    'version': '2.0',
    'category': 'GRAP - Custom',
    'description': """
Change eMail Template
====================================

Functionality
-------------

* Change Sale order eMail Template;
    * Add recovery moment information;

Limits
------
* Trick. The changes are done updating only translation file.
  GRAP doesn't need to communicate with non FR customers for the time
  being;

Copyright, Authors and Licence
------------------------------
    * Copyright: 2015-Today:
        * GRAP: Groupement Régional Alimentaire de Proximité;
    * Author:
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence: AGPL-3 (http://www.gnu.org/licenses/);""",
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'purchase',
        'sale',
        'sale_recovery_moment',
    ],
    'data': [
        'data/email_template.xml',
    ],
}
