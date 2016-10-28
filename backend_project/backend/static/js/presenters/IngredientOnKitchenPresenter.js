;(function (app, window) {
    'use strict';

    var deps = [];

    function Factory() {
        return IngredientOnKitchenPresenter;
    }

    app.factory('IngredientOnKitchenPresenter', deps.concat([Factory]));
    if (window.define) define(deps, Factory);

    function IngredientOnKitchenPresenter() {}

    IngredientOnKitchenPresenter.prototype.initIngredient = function(_ingredients, view, model){
        for(var i = 0; i < _ingredients.length; i++) {
            model.initIngredient(_ingredients[i], i);
            view.increaseIngredientInputViewTop();
            model.getRecipesByChefAndName(_ingredients[i].name, 'ingredients' + i, function() {});
        }

        model.updateSubIngredients();
    };

    IngredientOnKitchenPresenter.prototype.getRecipesByChefAndName = function(ingredientName, ingredientId, view, model) {
        model.getRecipesByChefAndName(ingredientName, ingredientId, function() {

        });
    };

    IngredientOnKitchenPresenter.prototype.checkIngredientChainable = function(aIngredient, view, model) {
        return model.checkIngredientChainable(aIngredient);
    };

    IngredientOnKitchenPresenter.prototype.getIngredientsSuggestion = function(ingredientInput, view, model) {
        model.getIngredientsSuggestion(ingredientInput, function(_ingredientsData) {
            view.fillIngredientsSuggestionData(_ingredientsData);
        });
    };

    IngredientOnKitchenPresenter.prototype.addSelectedIngredient = function(aIngredientName, view, model, callback) {
        var ingredientCount = model.addSelectedIngredient(aIngredientName);
        callback();
        model.saveIngredients();
        model.getRecipesByChefAndName(aIngredientName, 'ingredients' + ingredientCount);
    };

    IngredientOnKitchenPresenter.prototype.saveIngredients = function(view, model) {
       model.saveIngredients();
    };

    IngredientOnKitchenPresenter.prototype.removeIngredient = function(index, aIngredient, view, model) {
        model.removeIngredientAtIndex(index);
        var deleteIndex = model.getRecipesByNameIndexById(aIngredient.id);
        model.removeRecipesByNameAtIndex(deleteIndex);
        model.saveIngredients();
    };

    IngredientOnKitchenPresenter.prototype.showRecipesByIngredient = function(aIngredient, view , model) {
        var showIndex = model.getRecipesByNameIndexById(aIngredient.id);
        model.showRecipeByNameAtIndex(showIndex);
        view.setCurrentRecipesByNameByIndex(showIndex);
        return showIndex;
    };

    IngredientOnKitchenPresenter.prototype.hideRecipesByNameAtIndex = function(index, model) {
        model.hideRecipesByNameAtIndex(index);
    };

    IngredientOnKitchenPresenter.prototype.checkRecipeShowOrHide = function(aIngredient, view, model) {
        var checkIndex = model.getRecipesByNameIndexById(aIngredient.id);
        return model.checkRecipeShowOrHideAtIndex(checkIndex);
    };

    IngredientOnKitchenPresenter.prototype.searchRecipeByName = function(recipeName, aIngredient, view, model) {
        model.searchRecipeByName(recipeName, aIngredient, function(recipeName, aIngredient, recipesArray) {
            view.fillRecipeDataBySearch(recipeName, aIngredient, recipesArray);
        });
    };

    IngredientOnKitchenPresenter.prototype.getRecipesByNameAtIndex = function(index, model) {
        return model.getRecipesByNameAtIndex(index);
    };

    IngredientOnKitchenPresenter.prototype.toogleLinkToRecipe = function(recipeId, ingredient, view, model, callback) {
        if(recipeId === ingredient.linkRecipeId){
            model.clearRecipeLink(recipeId, ingredient.id);
        } else {
            model.saveRecipeLink(recipeId, ingredient.id);
        }

        callback();

        model.saveIngredients();

    };

    IngredientOnKitchenPresenter.prototype.loadMoreRecipes = function(aIngredient, view, model , callback) {
        var loadmoreIndex = model.getRecipesByNameIndexById(aIngredient.id);
        model.loadMoreRecipesByName(loadmoreIndex, function() {
            callback();
        });
    };

    IngredientOnKitchenPresenter.newInstance = function() {
        return new IngredientOnKitchenPresenter();
    };
})(app, this);
