/******************************************************************************
    Fix - Logo Multi Company Firefox for Odoo
    Copyright (C) 2013 GRAP (http://www.grap.coop)
    @author Sylvain LE GAL (https://twitter.com/legalsylvain)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
******************************************************************************/

openerp.fix_menu_logo_firefox = function (instance) {

    instance.web.WebClient = instance.web.WebClient.extend({
    /**
    Overload the JS function "instance.web.WebClient.update_logo()"
    Force to call the Python function "web/controllers/main.py/company_logo()"
    instead of using the url that is put in the session.
    */
        show_application: function() {
        /**
        Call another function to be sure that the logo image of the company
        is loaded. (adding timestamp)
        */
            this._super(parent);
            img = this.$('.oe_logo img').attr('src').replace("/web/binary/company_logo?", "/web/binary/company_logo_fix?");
            img += "&timestamp=" + new Date().getTime();
            this.$('.oe_logo img').attr('src', '').attr('src', img);
        },

        update_logo: function() {
    /** 
    Disable update_logo function
    */
        },
    });
};
