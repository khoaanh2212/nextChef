/**
 * Created by Kate on 3/22/16.
 */
;(function (app, window) {
    'use strict';

    var deps = ['AjaxService', '$q'];

    app.factory('AllergenModel', Factory);

    function Factory(AjaxService, $q) {
        AllergenModel.AjaxService = AjaxService;
        AllergenModel.$q = $q;
        return AllergenModel;
    }

    Factory.$inject = deps;

    if (window.define) define(Factory);

    function AllergenModel(ajaxService, Q) {
        this.ajaxService = ajaxService;
        this.Q = Q;
    }

    AllergenModel.prototype.loadAllergen = function(recipeId) {
        var url = '/0/recipes/' + recipeId + '/allergens';
        return this.ajaxService.ok('GET', url);
    };

    AllergenModel.prototype.onEdamamAnalyze = function(ingredient_list) {
        var requestOption = {timeout: 10000};
        var data = this._decorateEdamamRequest(ingredient_list);
        var url = EDAMAM_URL || '/0/recipes/edamam';
        return this.ajaxService.ok('POST', url, data, requestOption);
    };

    AllergenModel.prototype._decorateEdamamRequest = function(ingredient_list) {

        var ingredients = [];

        ingredient_list.forEach(function(ingredient) {
            ingredients.push(ingredient.name);
            if(ingredient.subIngredients) {
                ingredient.subIngredients.forEach(function(subIngr) {
                    ingredients.push(subIngr.name);
                });
            }
        });

        return ingredients;

    };

    AllergenModel.newInstance = function (ajaxService, Q) {
        ajaxService = ajaxService || AllergenModel.AjaxService.newInstance();
        Q = Q || AllergenModel.$q;
        return new AllergenModel(ajaxService, Q);
    }

})(app, this);
