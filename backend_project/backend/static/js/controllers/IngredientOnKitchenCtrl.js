;(function (app, window) {
    'use strict';

    var deps = ['IngredientOnKitchenModel', 'IngredientOnKitchenPresenter'];

    function Factory(IngredientOnKitchenModel, IngredientOnKitchenPresenter) {
        IngredientOnKitchenController.IngredientOnKitchenModel = IngredientOnKitchenModel;
        IngredientOnKitchenController.IngredientOnKitchenPresenter = IngredientOnKitchenPresenter;
        return IngredientOnKitchenController;
    }

    app.factory('IngredientOnKitchenController', deps.concat([Factory]));
    if (window.define) define(function (require) {
        return IngredientOnKitchenController;
    });

    function IngredientOnKitchenController(ingredientOnKitchenModel, ingredientOnKitchenPresenter) {
        this.ingredientModel = ingredientOnKitchenModel;
        this.ingredientPresenter = ingredientOnKitchenPresenter;

        this.ingredientInputTop = 57;
        this.ingredientInputTopOffset = 45;
        this.ingredientContentScrollTop = 0;
        this.ingredientInput = '';
        this.ingredientsSuggestion = [];
        this.showIngredientSuggestionResult = false;
        this.showIngredientsSuggestion = false;
        this.hoverIngredientSuggestion = false;
        this.showRecipesChain = false;
        this.currentRecipesByName = null;
    }

    IngredientOnKitchenController.prototype.initIngredient = function(_ingredients) {
        this.ingredientPresenter.initIngredient(_ingredients, this, this.ingredientModel);
    };

    IngredientOnKitchenController.prototype.getRecipesByChefAndName = function(ingredientName, ingredientId) {
        this.ingredientPresenter.getRecipesByChefAndName(ingredientName, ingredientId, this, this.ingredientModel);
    };

    IngredientOnKitchenController.prototype.checkIngredientChainable = function(aIngredient) {
        return this.ingredientPresenter.checkIngredientChainable(aIngredient, this, this.ingredientModel);
    };

    IngredientOnKitchenController.prototype.increaseIngredientInputViewTop = function() {
      this.ingredientInputTop += this.ingredientInputTopOffset;
    };

    IngredientOnKitchenController.prototype.reduceIngredientInputViewTop = function() {
      this.ingredientInputTop -= this.ingredientInputTopOffset;
    };

    IngredientOnKitchenController.prototype.getIngredientsSuggestion = function() {
       this.ingredientPresenter.getIngredientsSuggestion(this.ingredientInput, this, this.ingredientModel);
    };

    IngredientOnKitchenController.prototype.fillIngredientsSuggestionData = function(_ingredientsData) {
        this.ingredientsSuggestion = [];
        for(var i=0; i<_ingredientsData.length; i++){
            this.ingredientsSuggestion.push(_ingredientsData[i].name);
        }
        this.showIngredientSuggestionResult = true;
    };

    IngredientOnKitchenController.prototype.selectIngredientSuggestion = function(aIngredientName, callback) {
        this.increaseIngredientInputViewTop();
        this.ingredientPresenter.addSelectedIngredient(aIngredientName,  this, this.ingredientModel, function() {
            this.ingredientInput = '';
            callback();
        }.bind(this));
    };

    IngredientOnKitchenController.prototype.confirmIngredient = function(callback) {
        this.selectIngredientSuggestion(this.ingredientInput, callback);
    };

    IngredientOnKitchenController.prototype.saveIngredients = function() {
        this.showIngredientsSuggestion = false;
        this.showIngredientSuggestionResult = false;

        this.ingredientPresenter.saveIngredients(this, this.ingredientModel);
    };

    IngredientOnKitchenController.prototype.removeIngredient = function(index, aIngredient) {
        this.reduceIngredientInputViewTop();
        this.ingredientPresenter.removeIngredient(index, aIngredient, this, this.ingredientModel);
    };

    IngredientOnKitchenController.prototype.showRecipesByIngredient = function(aIngredient) {
		this.showRecipesChain = true;

		this.currentRecipesByName = {
            id: 'currentRecipes',
			name: '',
			recipes: [],
			show: false,
            page: 1,
            loadmore: false
		};

        return this.ingredientPresenter.showRecipesByIngredient(aIngredient, this, this.ingredientModel);

	};

    IngredientOnKitchenController.prototype.setCurrentRecipesByNameByIndex = function(index) {
        this.currentRecipesByName = this.ingredientPresenter.getRecipesByNameAtIndex(index, this.ingredientModel);
    };

    IngredientOnKitchenController.prototype.hideRecipesByNameAtIndex = function(index) {
       this.ingredientPresenter.hideRecipesByNameAtIndex(index, this.ingredientModel);
    };

    IngredientOnKitchenController.prototype.checkRecipeShowOrHide = function(aIngredient) {
        return this.ingredientPresenter.checkRecipeShowOrHide(aIngredient, this, this.ingredientModel);
    };

    IngredientOnKitchenController.prototype.searchRecipeByName = function(recipeName, aIngredient) {
        this.showRecipesChain = false;
        this.currentRecipesByName = {
            id: 'currentRecipes',
			name: '',
			recipes: [],
			show: true,
            page: 1,
            loadmore: false
		};

        this.ingredientPresenter.searchRecipeByName(recipeName, aIngredient, this, this.ingredientModel);

    };

    IngredientOnKitchenController.prototype.fillRecipeDataBySearch = function(recipesArray) {
        this.currentRecipesByName = (
                {
                    id: aIngredient.id,
                    name: recipeName,
                    recipes: recipesArray.data.results,
                    show: true,
                    page: 1,
                    loadmore: recipesArray.data.next !== null
                }
            );
    };

    IngredientOnKitchenController.prototype.toogleLinkToRecipe = function(recipeId, ingredient, callback) {
        this.ingredientPresenter.toogleLinkToRecipe(recipeId, ingredient, this, this.ingredientModel, function() {
           callback();
        });
    };

    IngredientOnKitchenController.prototype.loadmoreRecipes = function(aIngredient, callback) {
        this.ingredientPresenter.loadMoreRecipes(aIngredient, this, this.ingredientModel, function() {
           callback();
        });
    };

    IngredientOnKitchenController.prototype.setRecipeOnModel = function(recipe) {
        this.ingredientModel.setRecipe(recipe);
    };

    IngredientOnKitchenController.prototype.setChefOnModel = function(chef) {
        this.ingredientModel.setChef(chef);
    };

    IngredientOnKitchenController.newInstance = function(ingredientOnKitchenModel, ingredientOnKitchenPresenter) {
        return new IngredientOnKitchenController(
            ingredientOnKitchenModel || IngredientOnKitchenController.IngredientOnKitchenModel.newInstance(),
            ingredientOnKitchenPresenter || IngredientOnKitchenController.IngredientOnKitchenPresenter.newInstance());
    }

})(app, this);
