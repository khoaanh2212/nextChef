/**
 * Created by Kate on 3/24/16.
 */
;(function (app, window) {

    var deps = ['AllergenModel', 'AllergenPresenter', 'ToasterService'];

    app.factory('AllergenOnKitchenController', Factory);
    if (window.define) define(Factory);

    function Factory(AllergenModel, AllergenPresenter, ToasterService) {
        AllergenOnKitchenController.AllergenModel = AllergenModel;
        AllergenOnKitchenController.AllergenPresenter = AllergenPresenter;
        AllergenOnKitchenController.ToasterService = ToasterService;
        return AllergenOnKitchenController;
    }

    Factory.$inject = deps;


    function AllergenOnKitchenController(model, presenter, toaster, $scope) {
        this.model = model;
        this.presenter = presenter;
        this.toaster = toaster;

        this.events = this.presenter.show(this, model);

        this._initFn();
        this._initData();

        this.$scope = $scope;
        this.$scope.$on('updateAllergens', this.onIngredientAdded.bind(this))
    }

    AllergenOnKitchenController.prototype._initFn = function () {
        this.fn = {
            toggleAllergen: this.toggleAllergen.bind(this)
        };
    };

    AllergenOnKitchenController.prototype._initData = function () {
        this.data = {
            allergensList: ALL_ALLERGENS,
            selectedAllergens: {},
            isAnalyzingEdamam: false
        }
    };

    AllergenOnKitchenController.prototype.onLoad = function (saved_allergens) {
        if (!saved_allergens || !(saved_allergens instanceof Array))
            throw new Error('Saved allergens list cannot be empty');

        var self = this;

        this.allergens = saved_allergens;

        this.allergens.forEach(function (item) {
            self.data.selectedAllergens[item] = true
        });

    };

    AllergenOnKitchenController.prototype.toggleAllergen = function (index) {
        this.previous_allergens = JSON.parse(JSON.stringify(this.allergens));

        var hasAllergen = this.allergens.indexOf(this.data.allergensList[index]);
        if (hasAllergen > -1) {
            this.allergens.splice(hasAllergen, 1);
        } else {
            this.allergens.push(this.data.allergensList[index]);
        }

        this.updateAllergenForRecipe()
    };

    AllergenOnKitchenController.prototype.updateAllergenForRecipe = function () {
        this.$scope.recipe.allergen = this.allergens;
        this.$scope.recipe.deleted_allergens = this._getDeletedAllergens(this.previous_allergens, this.allergens);
        this.$scope.recipe.added_allergens = this._getAddedAllergens(this.previous_allergens, this.allergens);
        this.$scope.recipe.editAllergen();
    };

    AllergenOnKitchenController.prototype._getDeletedAllergens = function(previous, current) {
        var self = this;
        return previous.filter(function(p) {
            return !self._is_in(p, current)
        });
    };

    AllergenOnKitchenController.prototype._getAddedAllergens = function(previous, current) {
        var self = this;
        return current.filter(function(p) {
            return !self._is_in(p, previous)
        });
    };

    AllergenOnKitchenController.prototype._is_in = function(item, list) {
        return list.some(function(l_i) {
            return l_i == item;
        })
    };

    AllergenOnKitchenController.prototype.resetSelectedAllergens = function () {
        var self = this;
        this.data.allergensList.forEach(function (a) {
            self.data.selectedAllergens[a] = false;
        });
    };

    AllergenOnKitchenController.prototype.onIngredientAdded = function () {
        this.events.onUpdateAllergen(this.$scope.recipe.id);

    };

    AllergenOnKitchenController.prototype.onAllergenLoaded = function(allergens) {
        var self = this;
        self.resetSelectedAllergens();
        self.allergens = allergens;
        self.allergens.forEach(function (item) {
            self.data.selectedAllergens[item] = true;
        });
    };

    AllergenOnKitchenController.prototype.showError = function (error) {
        console.log(error);
    };

    AllergenOnKitchenController.newInstance = function ($scope, model, presenter, toaster) {
        model = model || AllergenOnKitchenController.AllergenModel.newInstance();
        presenter = presenter || AllergenOnKitchenController.AllergenPresenter.newInstance();
        toaster = toaster || AllergenOnKitchenController.ToasterService.newInstance();
        return new AllergenOnKitchenController(model, presenter, toaster, $scope);
    };


})(app, this);