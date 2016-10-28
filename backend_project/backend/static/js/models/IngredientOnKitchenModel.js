;(function (app, window) {
    'use strict';

    var deps = ['AjaxService'];

    function Factory(AjaxService) {
        IngredientOnKitchenModel.AjaxService = AjaxService;
        return IngredientOnKitchenModel;
    }

    app.factory('IngredientOnKitchenModel', Factory);
    if (window.define) define(Factory);

    Factory.$inject = deps;

    function IngredientOnKitchenModel(ajaxService) {
        this.ingredients = [];
        this.recipesByName = [];
        this.ajaxService = ajaxService;
    }

    IngredientOnKitchenModel.prototype.setRecipe = function(_recipe) {
        this.recipe = _recipe;
    };

    IngredientOnKitchenModel.prototype.setChef = function(_chef) {
        this.chef = _chef;
    };

    IngredientOnKitchenModel.prototype.initIngredient = function(_ingredient, index) {
        this.ingredients.push({
            id: 'ingredients' + index,
            name: _ingredient.name,
            linkRecipeId: _ingredient.linkRecipeId
        });
    };

    IngredientOnKitchenModel.prototype.getRecipesByChefAndName = function(ingredientName, ingredientId) {
        if(this.chef) {
                // check if exist
                for(var i = 0; i < this.recipesByName.length; i++) {
                    if(this.recipesByName[i].name === ingredientName){
                        this.recipesByName.push(
                            {
                                id: ingredientId,
                                name: ingredientName,
                                recipes: this.recipesByName[i].recipes,
                                show: false,
                                page: 1,
                                loadmore: this.recipesByName[i].loadmore
                            }
                        );
                        return;
                    }
                }
                // load
                this.chef.loadRecipesByName(ingredientName, 1).then(function(recipesArray) {
                    this.recipesByName.push(
                        {
                            id: ingredientId,
                            name: ingredientName,
                            recipes: recipesArray.data.results,
                            show: false,
                            page: 1,
                            loadmore: recipesArray.data.next !== null
                        }
                    );
                }.bind(this), function(error) {
                    this.recipesByName.push(
                        {
                            id: ingredientId,
                            name: ingredientName,
                            recipes: [],
                            show: false,
                            page: 1,
                            loadmore: false
                        }
                    );
                }.bind(this));
        }
    };

    IngredientOnKitchenModel.prototype.loadMoreRecipesByName = function(loadmoreIndex, callback) {
        this.chef.loadRecipesByName(this.recipesByName[loadmoreIndex].name, this.recipesByName[loadmoreIndex].page + 1).then(function(recipesArray) {
                for(var i = 0; i < recipesArray.data.results.length; i++) {
                    this.recipesByName[loadmoreIndex].recipes.push(recipesArray.data.results[i]);
                }
                this.recipesByName[loadmoreIndex].page += 1;
                this.recipesByName[loadmoreIndex].loadmore = (recipesArray.data.next !== null);
                this.currentRecipesByName = this.recipesByName[loadmoreIndex];

                callback();

            }, function(error) {
                this.recipesByName[loadmoreIndex].loadmore = false;
                this.currentRecipesByName.loadmore = false;

                callback();
            }
        );
    };

    IngredientOnKitchenModel.prototype.getIngredientsSuggestion = function(ingredientInput, callback) {
        this.recipe.getIngredientsSuggestion(ingredientInput, function(_ingredientsData) {
            callback(_ingredientsData);
        });
    };

    IngredientOnKitchenModel.prototype.addSelectedIngredient = function(aIngredientName) {
        var ingredientCount = this.ingredients.length;
		this.ingredients.push({
			id: 'ingredients' + ingredientCount,
			name: aIngredientName,
            linkRecipeId: null
		});
        return ingredientCount;
    };

    IngredientOnKitchenModel.prototype.saveIngredients = function() {
        var saveIngredients = [];
        for(var i = 0; i < this.ingredients.length; i++){
            saveIngredients.push(
                {
                    name: this.ingredients[i].name,
                    linkRecipeId: this.ingredients[i].linkRecipeId
                }
            );
        }
        this.recipe.ingredients = saveIngredients;
        this.recipe.editIngredients();
    };

    IngredientOnKitchenModel.prototype.removeIngredientAtIndex = function(index) {
        this.ingredients.splice(index,1);
    };

    IngredientOnKitchenModel.prototype.getRecipesByNameIndexById = function(id) {
        var index;
		for(var i = 0; i < this.recipesByName.length; i++) {
			if(this.recipesByName[i].id === id) {
				index = i;
				break;
			}
		}
        return index;
    };

    IngredientOnKitchenModel.prototype.removeRecipesByNameAtIndex = function(deleteIndex) {
        if(this.recipesByName.length > deleteIndex) {
			this.recipesByName.splice(deleteIndex,1);
		}
    };

    IngredientOnKitchenModel.prototype.getRecipesByNameAtIndex = function(getIndex) {
        return this.recipesByName[getIndex];
    };

    IngredientOnKitchenModel.prototype.showRecipeByNameAtIndex = function(showIndex) {
        this.recipesByName[showIndex].show = true;
    };

    IngredientOnKitchenModel.prototype.hideRecipesByNameAtIndex = function(index) {
        this.recipesByName[index].show = false;
    };

    IngredientOnKitchenModel.prototype.checkRecipeShowOrHideAtIndex = function(checkIndex) {
        if(this.recipesByName.length > checkIndex) {
			return this.recipesByName[checkIndex].show;
		}

		return false;
    };

    IngredientOnKitchenModel.prototype.searchRecipeByName = function(recipeName, aIngredient, callback) {
        this.chef.loadRecipesByName(recipeName, 1).then(function(recipesArray) {
            callback(recipeName, aIngredient, recipesArray);
        }, function(error) {

        });
    };

    IngredientOnKitchenModel.prototype.clearRecipeLink = function(recipeId, ingredientId) {
        for(var i = 0; i < this.ingredients.length; i++){
            if(this.ingredients[i].id === ingredientId){
                this.ingredients[i].linkRecipeId = null;
                break;
            }
        }
        this.updateSubIngredients();
    };

    IngredientOnKitchenModel.prototype.saveRecipeLink = function(recipeId, ingredientId) {
        for (var i = 0; i < this.ingredients.length; i++) {
            if (this.ingredients[i].id === ingredientId) {
                this.ingredients[i].linkRecipeId = recipeId;
                break;
            }
        }
        this.updateSubIngredients();
    };

    IngredientOnKitchenModel.prototype.updateSubIngredients = function() {
        var self = this;
        this.ingredients = this.ingredients.map(function(ingr) {
            if(ingr.linkRecipeId)
                self._getSubIngredients(ingr);
            else
                delete ingr.subIngredients;
            return ingr;
        });
    };

    IngredientOnKitchenModel.prototype._getSubIngredients = function(ingr) {
        var url = '/0/recipes/' + ingr.linkRecipeId + '/ingredients';
        this.ajaxService.ok('GET', url).then(function(response) {
            ingr.subIngredients = response.ingredients;
        });
    };

    IngredientOnKitchenModel.prototype.checkIngredientChainable = function(aIngredient) {
          if(this.recipesByName && this.recipesByName.length > 0) {
              for (var i = 0; i < this.recipesByName.length; i++) {
                  if (this.recipesByName[i].id === aIngredient.id && this.recipesByName[i].recipes.length > 0) {
                      return true;
                  }
              }
          }
          return false;
    };

    IngredientOnKitchenModel.newInstance = function(ajaxService) {
        ajaxService = ajaxService || IngredientOnKitchenModel.AjaxService.newInstance();
        return new IngredientOnKitchenModel(
            ajaxService
        );
    }

})(app, this);
