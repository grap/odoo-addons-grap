/******************************************************************************
    Point Of Sale - Improve Images module for OpenERP
    Copyright (C) 2014 GRAP (http://www.grap.coop)
    @author Julien WESTE
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

openerp.pos_improve_images = function(instance){
    var module = instance.point_of_sale;

    module.Product.prototype.get_image_url = function(){
        return instance.session.url('/web/binary/image', {model: 'product.product', field: 'image_medium', id: this.get('id')});
    };

    module.ProductCategoriesWidget.prototype.get_image_url = function(category){
        return instance.session.url('/web/binary/image', {model: 'pos.category', field: 'image_medium', id: category.id});
    };

//    var _initialize_ = module.ProductWidget.prototype.initialize;
    module.ProductWidget = module.ProductWidget.extend({
        renderElement: function() {
            this._super();
            if (!this.pos.product_image_list().has_image(this.model.id)){
                this.$('img').replaceWith(null);
                this.$('.product-img').addClass('product-img-without-image');
                this.$('.product-name').addClass('product-name-without-image');
            }
        },
    });

    /*************************************************************************
        Define : New Model 'ProductImage'
    */

    module.ProductImage = Backbone.Model.extend({
        has_image: function(){
            return this.attributes['has_image'];
        },
    });
    
    module.ProductImageCollection = Backbone.Collection.extend({
        model: module.ProductImage,
        has_image: function(id){
            return this._byId[id].has_image();
        },
    });

    /*
        Overload: PosModel.initialize() to define one list
    */
    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
        _initialize_.call(this, session, attributes);
        this.set({
            '_product_image_list': new module.ProductImageCollection(),
        });
    };

    module.PosModel.prototype.product_image_list = function(){
        return this.get('_product_image_list');
    }
    /*
        Overload: PosModel.load_server_data() function to get in memory
        if product has image.
    */
    var _load_server_data_ = module.PosModel.prototype.load_server_data;
    module.PosModel.prototype.load_server_data = function(){
        var self = this;
        var load_def = _load_server_data_.call(self).done(self.load_product_images_data());
        return load_def;
    },

    module.PosModel = module.PosModel.extend({
        load_product_images_data: function(){
            var self = this;
            var loaded = self.fetch(
                    'product.product',
                    ['has_image',],
                    [['available_in_pos', '=', true]])
                .then(function(products){
                    self.set({'_product_image_list' : new module.ProductImageCollection(products)});
                });
            return loaded;
        },
    });
};
