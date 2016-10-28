/**
 * Created by apium on 07/04/2016.
 */
;(function (app, window) {
    var deps = ['$http', '$q'];

    function Factory($http, $q) {
        IngredientDetailModel.$http = $http;
        IngredientDetailModel.$q = $q;
        return IngredientDetailModel;
    }

    app.service('IngredientDetailModel', Factory);
    if (window.define) define(Factory);
    Factory.$inject = deps;

    function IngredientDetailModel($http, $q) {
        this.$http = $http;
        this.$q = $q;
    }

    IngredientDetailModel.newInstance = function ($http, $q) {
        return new IngredientDetailModel(
            $http || IngredientDetailModel.$http,
            $q || IngredientDetailModel.$q
        );
    };

    IngredientDetailModel.prototype.initModel = function() {
        return this.$http.get('/0/recipes/' + RECIPE_ID + '/details').then(function(response) {
            this.setIngredientList(response.data.ingredients);
            this.getTotal(response.data.ingredients);
            this.calculator();
            return this.toDTO();
        }.bind(this));
    };

    IngredientDetailModel.prototype.setIngredientList = function(ingredients) {
        this.ingredients = ingredients;
    };

    IngredientDetailModel.prototype.getTotal = function(ingredient) {
        var total = 0;
        var self = this;
        ingredient.forEach(function(item) {
            if (!item.price) self.hasEmptyIngredient = true;
            else total += +item.price;
        });
        this.total = total;
    };

    IngredientDetailModel.prototype.calculator = function() {
        this.totalCostPerPortion = roundTwoDecimal(this.total / SERVINGS);
        this.grossProfit = roundTwoDecimal((this.totalCostPerPortion / 25) * 75);
        this.singlePortion = this.totalCostPerPortion + this.grossProfit;
        this.VAT = roundTwoDecimal(this.singlePortion * 1.2);
    };

    IngredientDetailModel.prototype.toDTO = function() {
        return {
            ingredients: this.ingredients,
            total: this.total,
            totalCostPerPortion: this.totalCostPerPortion,
            grossProfit: this.grossProfit,
            foodCost: this.totalCostPerPortion,
            singlePortion: this.singlePortion,
            VAT: this.VAT,
            hasEmptyIngredient: this.hasEmptyIngredient || false
        };
    };

})(app, this);

function roundTwoDecimal(number) {
    return Math.round(number * 100) / 100;
}