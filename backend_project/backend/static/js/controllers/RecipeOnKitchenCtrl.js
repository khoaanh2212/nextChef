/**
 * Created by kate on 06/05/2016.
 */

;(function (app, window) {

    app.factory('RecipeOnKitchenController', Factory);
    if (window.define) define(Factory);

    function Factory() {
        return RecipeOnKitchenController;
    }


    function RecipeOnKitchenController($scope) {
        this._initFn();
        this.$scope = $scope;
    }

    RecipeOnKitchenController.prototype._initFn = function () {
        this.fn = {
            savePublic: this.savePublic.bind(this),
            savePrivate: this.savePrivate.bind(this)
        };
    };

    RecipeOnKitchenController.prototype.savePublic = function() {
        this.$scope.recipe.private = false;
        this.$scope.publish();
    };

    RecipeOnKitchenController.prototype.savePrivate = function() {
        this.$scope.recipe.private = true;
        this.$scope.publish();
    };

    RecipeOnKitchenController.prototype.showError = function (error) {
        console.log(error);
    };

    RecipeOnKitchenController.newInstance = function ($scope) {
        return new RecipeOnKitchenController($scope);
    };


})(app, this);