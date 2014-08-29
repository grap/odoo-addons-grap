/******************************************************************************
    Point Of Sale - Restaurant module for OpenERP
    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

openerp.pos_restaurant = function (instance) {
    module = instance.point_of_sale;
    _t = instance.web._t;

    /*************************************************************************
        Define : CoversOrderWidget that display the covers quantity
        of the current pos order and buttons to select current covers quantity.
    */
    module.CoversOrderWidget = module.PosBaseWidget.extend({
        template: 'CoversOrderWidget',

        /* Overload Section */
        init: function(parent, options){
            this._super(parent,options);
            this.pos.bind('change:selectedOrder', this.refresh, this);
        },

        start: function(){
            this._super();
            this._build_widgets();
        },

        /* Custom Section */
        refresh: function(){
            this.renderElement();
            this._build_widgets();
        },

        _build_widgets: function(){
            // Create a button to open the covers popup
            this.select_covers_button = new module.HeaderButtonWidget(this,{
                label:_t('Covers'),
                action: function(){
                    self.screen_selector.show_popup('select-covers');
                },
            });
            this.select_covers_button.replace($('.placeholder-SelectCoversButton'));
            this.select_covers_button.renderElement();
        },

        get_name: function(){
            return this.pos.get('selectedOrder').get_covers();
        },
    });

    /*************************************************************************
        Define : CoversWidget that display a covers quantity
    */
    module.CoversWidget = module.PosBaseWidget.extend({
        template: 'CoversWidget',

        /* Overload Section */
        init: function(parent, options) {
            this._super(parent,options);
            this.quantity = options.quantity;
        },

        renderElement: function() {
            this._super();
            var self = this;
            $("a", this.$el).click(function(e){
                self.pos.get('selectedOrder').set_covers(self.quantity);
                self.pos_widget.covers_order.refresh();
                self.pos_widget.screen_selector.set_current_screen('products');
            });
        },
    });

    /*************************************************************************
        Define : CoversListScreenWidget that display a list of covers.
    */
    module.CoversListScreenWidget = module.ScreenWidget.extend({
        template:'CoversListScreenWidget',

        /* Overload Section */
        start: function() {
            this._super();
            var self = this;

            // Display covers list
            this.covers_list = [];
            for(var i = 0, len = this.pos.get('max_covers') + 1; i < len; i++){
                var covers = new module.CoversWidget(this, {
                    quantity: i,
                });
                this.covers_list.push(covers);
                covers.appendTo(this.$('.covers-list'));
            }

            // Display scrollbar
            this.scrollbar = new module.ScrollbarWidget(this,{
                target_widget:   this,
                target_selector: '.covers-list-scroller',
                on_show: function(){
                    self.$('.covers-list-scroller').css({'padding-right':'62px'},100);
                },
                on_hide: function(){
                    self.$('.covers-list-scroller').css({'padding-right':'0px'},100);
                },
            });
            this.scrollbar.replace(this.$('.placeholder-ScrollbarWidget'));
        },
    });

    /*************************************************************************
        Define : SelectCoversPopupWidget that display a pop up to select
        covers quantity
    */
    module.SelectCoversPopupWidget = module.PopUpWidget.extend({
        template:'SelectCoversPopupWidget',

        /* Overload Section */
        start: function(){
            this._super();
            this.covers_list_widget = new module.CoversListScreenWidget(this,{});
            this.covers_list_widget.renderElement();
            this.covers_list_widget.replace($('.placeholder-CoversListScreenWidget'));
            this.$('#covers-cancel').off('click').click(function(){
                self.pos_widget.screen_selector.set_current_screen('products');
            });
        },

    });

    /*************************************************************************
        Define : TableOrderWidget that display the name of the table
        of the current pos order and buttons to select or remove current table.
    */
    module.TableOrderWidget = module.PosBaseWidget.extend({
        template: 'TableOrderWidget',

        /* Overload Section */
        init: function(parent, options){
            this._super(parent,options);
            this.pos.bind('change:selectedOrder', this.refresh, this);
        },

        start: function(){
            this._super();
            this._build_widgets();
        },

        /* Custom Section */
        refresh: function(){
            this.renderElement();
            this._build_widgets();
        },

        _build_widgets: function(){
            // Create a button to open the table popup
            this.select_table_button = new module.HeaderButtonWidget(this,{
                label:_t('Table'),
                action: function(){
                    self.screen_selector.show_popup('select-table');
                },
            });
            this.select_table_button.replace($('.placeholder-SelectTableButton'));
            this.select_table_button.renderElement();

            if (this.pos.get('selectedOrder').get_table_name() !== ""){
                // Create a button to remove the current table
                this.remove_table_button = new module.HeaderButtonWidget(this,{
                    label:_t('Del.'),
                    action: function(){
                        this.pos.get('selectedOrder').set_table(undefined);
                        this.pos_widget.table_order.refresh();
                        this.hide();
                    },
                });
                this.remove_table_button.replace($('.placeholder-RemoveTableButton'));
                this.remove_table_button.renderElement();
            }
        },

        get_name: function(){
            return this.pos.get('selectedOrder').get_table_name();
        },
    });

    /*************************************************************************
        Define : TableWidget that display a table
    */
    module.TableWidget = module.PosBaseWidget.extend({
        template: 'TableWidget',

        /* Overload Section */
        init: function(parent, options) {
            this._super(parent,options);
            this.model = options.model;
        },

        renderElement: function() {
            this._super();
            var self = this;
            this.$('img').replaceWith(this.pos_widget.image_cache.get_image(this.model.get_image_url()));
            $("a", this.$el).click(function(e){
                self.pos.get('selectedOrder').set_table(self.model.toJSON());
                self.pos_widget.table_order.refresh();
                self.pos_widget.screen_selector.set_current_screen('products');
            });
        },
    });

    /*************************************************************************
        Define : TableListScreenWidget that display a list of tables.
    */
    module.TableListScreenWidget = module.ScreenWidget.extend({
        template:'TableListScreenWidget',

        /* Overload Section */
        start: function() {
            this._super();
            var self = this;

            // Display table list
            this.table_list = [];
            var tables = this.pos.get('table_list') || [];
            for(var i = 0, len = tables.models.length; i < len; i++){
                var table = new module.TableWidget(this, {
                    model: tables.models[i],
                });
                this.table_list.push(table);
                table.appendTo(this.$('.table-list'));
            }

            // Display scrollbar
            this.scrollbar = new module.ScrollbarWidget(this,{
                target_widget:   this,
                target_selector: '.table-list-scroller',
                on_show: function(){
                    self.$('.table-list-scroller').css({'padding-right':'62px'},100);
                },
                on_hide: function(){
                    self.$('.table-list-scroller').css({'padding-right':'0px'},100);
                },
            });
            this.scrollbar.replace(this.$('.placeholder-ScrollbarWidget'));
        },
    });

    /*************************************************************************
        Define : SelectTablePopupWidget that display a pop up to search
        and select table.
    */
    module.SelectTablePopupWidget = module.PopUpWidget.extend({
        template:'SelectTablePopupWidget',

        /* Overload Section */
        start: function(){
            this._super();
            var self = this;
            this.table_list_widget = new module.TableListScreenWidget(this,{});
        },

        show: function(){
            this._super();
            var self = this;
            this.table_list_widget.renderElement();
            this.table_list_widget.replace($('.placeholder-TableListScreenWidget'));
            this.$('#table-cancel').off('click').click(function(){
                self.pos_widget.screen_selector.set_current_screen('products');
            });
        },

    });


    /*************************************************************************
        Overload : PosWidget to include button in PosOrderHeaderWidget widget
        to select or unselect tables
    */
    module.PosWidget = module.PosWidget.extend({

        /* Overload Section */
        build_widgets: function(){
            this._super();
            var self = this;
            if (this.pos.get('table_list').length != 0){
                // create a pop up 'select-table' to search and select tables
                this.select_table_popup = new module.SelectTablePopupWidget(this, {});
                this.select_table_popup.appendTo($('.point-of-sale'));
                this.select_table_popup.hide();
                this.screen_selector.popup_set['select-table'] = this.select_table_popup;

                // Add a widget to manage table
                this.table_order = new module.TableOrderWidget(this,{});
                this.table_order.appendTo(this.$('#pos_order_header'));
            }
            if (this.pos.get('max_covers') > 0){
                // create a pop up 'select-covers' to covers quantity
                this.select_covers_popup = new module.SelectCoversPopupWidget(this, {});
                this.select_covers_popup.appendTo($('.point-of-sale'));
                this.select_covers_popup.hide();
                this.screen_selector.popup_set['select-covers'] = this.select_covers_popup;

                // Add a widget to manage covers
                this.covers_order = new module.CoversOrderWidget(this,{});
                this.covers_order.appendTo(this.$('#pos_order_header'));
            }
        },
    });

    /*************************************************************************
        Define : New Model 'module.Table'
    */
    module.Table = Backbone.Model.extend({
        get_image_url: function(){
            return instance.session.url('/web/binary/image', {model: 'pos.table', field: 'image', id: this.get('id')});
        },
    });

    module.TableCollection = Backbone.Collection.extend({
        model: module.Table,
    });

    /*************************************************************************
        Overload : Model 'module.Order'
//    */
    module.Order = module.Order.extend({
        set_covers: function(covers){
            this.set('covers',covers);
        },
        get_covers: function(){
            return this.get('covers');
        },
        set_table: function(table){
            this.set('table',table);
        },
        get_table: function(){
            return this.get('table');
        },
        get_table_name: function(){
            var table = this.get('table');
            return table ? table.name : "";
        },
    });

    var _initialize_Order_ = module.Order.prototype.initialize;
    module.Order.prototype.initialize = function(attributes){
        _initialize_Order_.call(this, attributes);
        this.set({
            'table': null,
            'covers': 0,
        });
    };

    var _exportAsJSON_Order_ = module.Order.prototype.exportAsJSON;
    module.Order.prototype.exportAsJSON = function(){
        result = _exportAsJSON_Order_.call(this);
        if (this.pos.get('group_restaurant_user')){
            result['table_id'] = this.get('table') ? this.get('table').id : undefined;
            result['covers'] = this.get('covers');
        }
        return result;
    };

    /*************************************************************************
        Overload : Model 'module.PosModel'
    */
    /*
        Overload: PosModel.initialize() to define one new list.
        'table_list' are the list of all tables available;
    */
    var _initialize_PosModel_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
         _initialize_PosModel_.call(this, session, attributes);
        this.set({
            'group_restaurant_user': false,
            'table_list': new module.TableCollection(),
            'max_covers': 0,
        });
    };

    /*
        Overload: PosModel.load_server_data() function to get in memory
        tables.
    */
    var _load_server_data_PosModel_ = module.PosModel.prototype.load_server_data;
    module.PosModel.prototype.load_server_data = function(){
        var self = this;
        var load_def = _load_server_data_PosModel_.call(self).then(function(){
                return self.load_tables_data();
            });
        return load_def;
    };

    module.PosModel = module.PosModel.extend({
        load_tables_data: function(){
            var self = this;
            var res_users_obj = new instance.web.Model('res.users');
            
            var loaded = res_users_obj.call(
                'has_group',
                ['pos_restaurant.res_group_restaurant_user'],
                undefined,{}
            ).then(function(result){
                self.set({'group_restaurant_user' : result});
                if (result){
                    return self.fetch(
                        'pos.table',
                        ['name'],
                        [['shop_id', '=', self.get('shop').id]]
                    ).then(function(tables){
                        self.set({'table_list' : new module.TableCollection(tables)});
                        return self.fetch(
                            'sale.shop',
                            ['max_covers'],
                            [['id', '=', self.get('shop').id]]
                        ).then(function(max_covers){
                            self.set({'max_covers' : max_covers[0].max_covers});
                        });
                    });
                }else{
                    return true;
                }
             });
            return loaded;
        },
    });
};

