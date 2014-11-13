/******************************************************************************
    Point Of Sale - Restaurant module for OpenERP
    Copyright (C) 2014 GRAP (http://www.grap.coop)
    @author Sylvain LE GAL (https://twitter.com/legalsylvain)

    Some part of this code come from Odoo point Of Sale Module.
    Copyright (C) Odoo (http://www.odoo.com)

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


openerp.pos_improve_posbox = function (instance) {
    // Define a new namespace
    instance.pos_improve_posbox = {};

    // Link the tag 'pos.posbox' to the widget
    instance.web.client_actions.add('pos.posbox', 'instance.pos_improve_posbox.PosPoxReceiptWidget');

    // short variables
    custom_module = instance.pos_improve_posbox;
    pos_module = instance.point_of_sale;
    _t = instance.web._t;


    /*************************************************************************
        Overload : PosModel to load the extra-value pos_config.proxy_ip
    */
    var _load_server_data_ = pos_module.PosModel.prototype.load_server_data;
    pos_module.PosModel.prototype.load_server_data = function(){
        var self = this;
        var load_def = _load_server_data_.call(self).done(self.load_customers_data());
        return load_def;
    },
    pos_module.PosModel = pos_module.PosModel.extend({
        load_customers_data: function(){
            var self = this;
            var loaded = self.fetch('pos.session',
                    ['id', 'config_id'], [
                        ['state', '=', 'opened'],
                        ['user_id', '=', self.session.uid]])
                .then(function(session){
                    // Get the session of the user
                    return self.fetch('pos.config',
                            ['id', 'proxy_ip'], [
                                ['id', '=', session[0].config_id[0]]])
                        .then(function(session){
                            // get the config of the session of the user
                            // and reset proxy_ip value to the ProxyDevice Object
                            self.proxy.connection.setup(session[0].proxy_ip);
                        });
                });
            return loaded;
        },
    });

    /*************************************************************************
        Define : PosPoxReceiptWidget that manage communication between 
        the point of sale backoffice and the posbox and display the status 
        of the print receipt.
    */
//    module.PosPoxReceiptWidget = instance.web.Widget.extend({
//        template: 'PosPoxReceiptWidget',

//        /* **************** */
//        /* Overload Section */
//        /* **************** */
//        init: function(parent, options){
//            //url =  || 'http://192.168.1.16:8069';
//            this.connection = new instance.web.JsonRPC();
//            this.connection.setup(url);
//            this.receipt = options.context.receipt;
//            this.timeout = option.context.timeout;
//            this.notifications = {};
//            this.connection.session_id = _.uniqueId('PosPoxReceiptWidget');
//            this._super(parent,options);
//        },

//        start: function(){
//            this._super();
//            var self = this;
//            this._message('print_receipt',{receipt: this.receipt});
//        },

//        renderElement: function(){
//            this._super();
//        },

//        /* ************** */
//        /* Custom Section */
//        /* ************** */


//        _message : function(name, params){
//            var self = this;
//            var ret = new $.Deferred();
//            var callbacks = this.notifications[name] || [];
//            for(var i = 0; i < callbacks.length; i++){
//                callbacks[i](params);
//            }
//            this.connection.rpc('/pos/' + name, params || {}
//            ).done(function(result) {
//                console.log(result); //TODO
//                ret.resolve(result);
//            }).fail(function(error) {
//                console.log(error); //TODO
//                ret.reject(error);
//            });
//            setTimeout(function() {
//                console.log('sorry'); //TODO
//                ret.reject('timeout');
//            }, this.timeout);
//            return ret;
//        },

//    });

};

