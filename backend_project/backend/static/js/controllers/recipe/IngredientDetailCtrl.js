/**
 * Created by apium on 07/04/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['$scope', 'IngredientDetailPresenter', 'IngredientDetailModel'];

    app.controller("IngredientDetailController", deps.concat([function ($scope, presenter, model) {
        IngredientDetailController.$scope = $scope;
        IngredientDetailController.presenter = presenter;
        IngredientDetailController.model = model;
        return IngredientDetailController.newInstance();
    }]));

    if (window.define) define(function () {
        return IngredientDetailController;
    });

    function IngredientDetailController($scope, presenter, model) {
        this.$scope = $scope;
        this.presenter = presenter;
        this.model = model;
        this.$scope.events = this.presenter.show(this, this.model);
        this._initFn();
    }

    IngredientDetailController.newInstance = function ($scope, presenter, model) {
        return new IngredientDetailController(
            $scope || IngredientDetailController.$scope,
            presenter || IngredientDetailController.presenter.newInstance(),
            model || IngredientDetailController.model.newInstance()
        );
    };

    IngredientDetailController.prototype._initFn = function () {
        this.$scope.fn = {
            linkRecipe: this.linkRecipe.bind(this),
            publishGrossProfitEvent: this.publishGrossProfitEvent.bind(this),
            publishFoodCostEvent: this.publishFoodCostEvent.bind(this),
            publishVatEvent: this.publishVatEvent.bind(this),
            publishServings: this.publishServings.bind(this)
        };

        this.$scope.filterNumber = function ($event) {
            if (isNaN(String.fromCharCode($event.keyCode))) {
                $event.preventDefault();
            }
        };
    };

    IngredientDetailController.prototype.init = function (response) {
        this.$scope.ingredientList = response.ingredients;
        this.decorateListIngredient();
        this.$scope.total = response.total;
        this.$scope.totalCostPerPortion = response.totalCostPerPortion;
        this.$scope.singlePortion = response.singlePortion;
        this.$scope.VAT = response.VAT;
        this.$scope.hasEmptyIngredient = response.hasEmptyIngredient;
        this.$scope.isWaiting = false;
        this.subcribe();
    };

    IngredientDetailController.prototype.subcribe = function () {
        this.$scope.$on('broadcast_finish_update_pricing', function (event, args) {
            this.$scope.isWaiting = false;
            if (args.success == true) {
                if (this.$scope.oldServings != this.$scope.servings && this.$scope.oldServings != 0) {
                    this.$scope.oldServings = this.$scope.servings;
                    this.$scope.events.onLoad();
                }
            }


        }.bind(this));
    };

    IngredientDetailController.prototype.handleListIngredientAfterChangeServings = function () {
        var n = this.$scope.servings / this.$scope.oldServings;
        for (var i = 0; i < this.$scope.ingredientList.length; i++) {
            this.$scope.ingredientList[i].quantity = n * this.$scope.ingredientList[i].quantity;
            this.$scope.ingredientList[i].price = n * this.$scope.ingredientList[i].price;
        }
    };

    IngredientDetailController.prototype.showError = function (error) {
        console.log(error);
    };

    IngredientDetailController.prototype.linkRecipe = function (item) {
        var link = '/recipe/' + encodeURI(item.name) + '-' + item.subrecipe_id;
        window.open(link, '_blank')
    };

    IngredientDetailController.prototype.publishGrossProfitEvent = function () {
        this.$scope.food_cost = 100 - this.$scope.gross_profit;
        this.$scope.isWaiting = true;
        this.$scope.$emit('emit_GrossProfit_FoodCost', {
            gross_profit: this.$scope.gross_profit,
            food_cost: this.$scope.food_cost
        });
    };

    IngredientDetailController.prototype.publishFoodCostEvent = function () {
        this.$scope.gross_profit = 100 - this.$scope.food_cost;
        this.$scope.isWaiting = true;
        this.$scope.$emit('emit_GrossProfit_FoodCost', {
            gross_profit: this.$scope.gross_profit,
            food_cost: this.$scope.food_cost
        });
    };

    IngredientDetailController.prototype.publishVatEvent = function () {
        this.$scope.isWaiting = true;
        this.$scope.$emit('emit_VAT', {
            vat: this.$scope.vat
        });
    };

    IngredientDetailController.prototype.publishServings = function () {
        if (this.$scope.servings != '' && this.$scope.servings != '0') {
            this.$scope.isWaiting = true;
            this.$scope.$emit('emit_Servings', {
                servings: this.$scope.servings, oldServings: this.$scope.oldServings
            });
        }
    };

    IngredientDetailController.prototype.decorateListIngredient = function () {
        for (var i = 0; i < this.$scope.ingredientList.length; i++) {
            var quantity = parseFloat(this.$scope.ingredientList[i].quantity);
            this.$scope.ingredientList[i].quantity = quantity.toString();
        }
    };

})(app, this);