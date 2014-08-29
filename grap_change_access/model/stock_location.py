# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Access module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

from openerp.osv.orm import Model


class stock_location(Model):
    _inherit = "stock.location"

    def _complete_name(self, cr, uid, ids, name, args, context=None):
        """ Forms complete name of location from parent location to child
        location.
        @return: Dictionary of values
        """
        res = {}
        for m in self.browse(cr, uid, ids, context=context):
            names = [m.name]
            parent = m.location_id
            while parent:
                try:
                    names.append(parent.name)
                    parent = parent.location_id
                except:
                    parent = None
            res[m.id] = ' / '.join(reversed(names))
        return res
