# -*- encoding: utf-8 -*-
##############################################################################
#
#    Export to EBP module for OpenERP
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    based on a Numerigraphe module
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

import base64
import cStringIO
import os
import codecs
import smbc
from unidecode import unidecode

import tools
from tools.translate import _
from openerp.osv import fields, osv
import logging
_logger = logging.getLogger(__name__)

class account_unexport_ebp(osv.TransientModel):
    _name = "account.unexport.ebp"

#Columns Section
    _columns = {
    }

    def unexport(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        unexport_ids = context.get('active_ids', False)
        am_obj = self.pool.get('account.move')
        am_obj.write(cr, uid, unexport_ids, {'exported_ebp_id': False}, context=context)
        #TODO: find the file in ebp.export model and remove the move lines
        return ids
