# -*- encoding: utf-8 -*-
##############################################################################
#
#    Module - Backup Files module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

import os
from ftplib import FTP
from os import path

from openerp.osv.orm import Model
from openerp.osv import osv, fields
from openerp import tools
from openerp.tools.translate import _


class ir_backup(Model):
    _name = 'ir.backup'

    _CONNEXION_TYPE = [
        ('ftp', 'FTP'),
    ]

    # Column Section
    _columns = {
        'name': fields.char('Name', required=True),
        'local_folder': fields.char('Local Folder'),
        'distant_folder': fields.char('Distant Folder'),
        'ftp_hostname': fields.char('FTP Host Name'),
        'ftp_port': fields.integer('FTP Port'),
        'ftp_username': fields.char('FTP User Name'),
        'ftp_password': fields.char('FTP Password'),
        'connexion_type': fields.selection(
            _CONNEXION_TYPE, 'Connexion Type'),
    }

    _defaults = {
        'ftp_port': 21,
    }

    # Action Function
    def test_local_access_right(self, cr, uid, ids, context=None):
        for ib in self.browse(cr, uid, ids, context=context):
            if not path.exists(ib.local_folder):
                raise osv.except_osv(
                    _("Local Folder Doesn't Exist!"),
                    _("'%s' is unreachable!" %(ib.local_folder)))
            try:
                filename = ib.local_folder + "/" + "test.txt"
                fo = open(filename, "wb")
                fo.close()
            except Exception, e:
                raise osv.except_osv(
                    _("Creation of a Test file Failed!"),
                    _("Here is what we got instead:\n %s") % tools.ustr(e))
            try:
                os.remove(filename)
            except Exception, e:
                raise osv.except_osv(
                    _("Deletion of the Test file Failed!"),
                    _("Here is what we got instead:\n %s") % tools.ustr(e))
        raise osv.except_osv(
            _("Write Access to Local Folder Test Succeeded!"),
            _("Everything seems properly set up!"))

    def test_ftp_connection(self, cr, uid, ids, context=None):
        for ib in self.browse(cr, uid, ids, context=context):
            try:
                ftp = self._ftp_connect(cr, uid, ib, context=context)
                self._ftp_disconnect(cr, uid, ftp, context=context)
            except Exception, e:
                raise osv.except_osv(
                    _("FTP Connection Test Failed!"),
                    _("Here is what we got instead:\n %s") % tools.ustr(e))
        raise osv.except_osv(
            _("FTP Connection Test Succeeded!"),
            _("Everything seems properly set up!"))

    def execute_backup(self, cr, uid, ids, context=None):
        try:
            currdir=os.getcwd()
            for ib in self.browse(cr, uid, ids, context=context):
                os.chdir(ib.local_folder)
                # connexion
                if ib.connexion_type in 'ftp':
                    self._ftp_backup(cr, uid, ib, context=context)
                else:
                    raise NotImplementedError(
                        "Connexion Type '%s' is not implemented" %(
                            ib.connexion_type))
        finally:
            os.chdir(currdir)
        return True

    # Private FTP function
    def _ftp_connect(self, cr, uid, ir_backup, context=None):
        ftp = FTP(ir_backup.ftp_hostname)
        ftp.login(ir_backup.ftp_username, ir_backup.ftp_password)
        if ir_backup.distant_folder:
            ftp.cwd(ir_backup.distant_folder)
        return ftp

    def _ftp_disconnect(self, cr, uid, ftp, context=None):
        ftp.close()

    def _ftp_backup(self, cr, uid, ir_backup, context=None):
            ftp = self._ftp_connect(cr, uid, ir_backup, context=context)
            data = []
            items = []
            tmp_ls = []
            ftp.retrlines('MLSD', tmp_ls.append)
            for entry in tmp_ls:
                values = {}
                tmp = entry.split("; ", 1)
                values['name']= tmp[1]
                for vals in tmp[0].split(";"):
                    values[vals.split("=")[0]] = vals.split("=")[1]
                if values['name'] not in ('.', '..'):
                    items.append(values)
            # TODO check datetime
            
            # TODO write a function to get file
            ## TODO write a recursive function to get folder
            for item in items:
                if item['type'] == 'file':
                    print "***********"
                    print item['name']
                    full_name = os.path.normpath(os.path.join(
                        os.path.normpath(ir_backup.local_folder),
                        os.path.normpath(item['name'])))
                    ftp.retrbinary(
                        'RETR %s' %(item['name']),
                        open(full_name, 'wb').write)
            self._ftp_disconnect(cr, uid, ftp, context=context)
