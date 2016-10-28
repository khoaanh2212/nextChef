/**
 * Created by apium on 01/04/2016.
 */
;(function (app, window) {
    var deps = ['$http', '$q'];

    function Factory($http, $q) {
        IngredientModel.$http = $http;
        IngredientModel.$q = $q;
        return IngredientModel;
    }

    app.service('IngredientModel', Factory);
    if (window.define) define(Factory);
    Factory.$inject = deps;

    function IngredientModel($http, $q) {
        this.$http = $http;
        this.$q = $q;
        this.ingredientList = [];
        this.allergens = [];
        this.ingredients = [];
        this.recipes = [];
        this.isShowMoreIngredient = true;
        this.isShowMoreRecipe = true;
    }

    IngredientModel.newInstance = function ($http, $q) {
        return new IngredientModel(
            $http || IngredientModel.$http,
            $q || IngredientModel.$q
        );
    };

    IngredientModel.prototype.getIngredientList = function () {
        return this.$http.get('/0/recipes/' + RECIPE_ID + '/details')
            .then(function (response) {
                this.setAllergens(response.data.allergens);
                return this.decorateIngredientList(response.data.ingredients);
            }.bind(this))
            .then(function (ingredients) {
                this.setIngredientList(ingredients);
                return this.toDTO();
            }.bind(this));
    };

    IngredientModel.prototype.decorateIngredientList = function (ingredients) {
        return ingredients.map(function (item) {
            if (item.type === 'recipe') {
                var amount = item.amount.length > 15 ? item.amount.substring(0, 14) + '...' : item.amount
                return {
                    id: item.id,
                    name: amount + ' ' + item.name,
                    chef_name: item.owner_name,
                    link: '/recipe/' + encodeURI(item.name) + '-' + item.subrecipe_id
                };
            } else {
                var measure = item.measure.toLowerCase() == item.name.toLowerCase() ? '' : item.measure;
                if (item.name.indexOf(item.measure) > -1)
                    var name = parseFloat(item.quantity).toString() + ' ' + item.name;
                else
                    var name = parseFloat(item.quantity).toString() + ' ' + measure + ' ' + item.name;

                return {
                    id: item.id,
                    name: name
                }
            }
        })
    };

    IngredientModel.prototype.makeDropdownList = function (ingredientText) {
        if (!ingredientText) {
            return {isShow: false};
        }
        if (this.ingredientText !== ingredientText) {
            this.isShowMoreIngredient = true;
        }
        this.ingredientText = ingredientText;
        this.ingredientPage = 1;
        this.recipePage = 1;
        var ingredients = this.$http.get('/0/ingredients?filter=' + this.ingredientText + '&page=' + this.ingredientPage);
        var recipes = this.$http.get('/0/subrecipes?filter=' + this.ingredientText + '&page=' + this.recipePage);
        return this.$q.all([ingredients, recipes]).then(function (response) {
            this.setIngredients(response[0].data);
            this.setRecipes(response[1].data);
            return this.toDropdownDTO();
        }.bind(this));
    };

    IngredientModel.prototype.setIngredientList = function (ingredients) {
        this.ingredientList = ingredients;
    };

    IngredientModel.prototype.setAllergens = function (allergens) {
        this.allergens = allergens;
    };

    IngredientModel.prototype.setMessage = function (message) {
        this.message = message;
    }

    IngredientModel.prototype.setIngredients = function (ingredients) {
        this.ingredients = ingredients;
    };

    IngredientModel.prototype.setRecipes = function (recipes) {
        this.recipes = recipes;
    };

    IngredientModel.prototype.setSelectedIngredient = function (ingredient) {
        this.selectedIngredient = ingredient;
    };

    IngredientModel.prototype.toDropdownDTO = function () {
        return {
            ingredients: this.ingredients,
            isShowMoreIngredient: this.isShowMoreIngredient,
            recipes: this.recipes,
            isShowMoreRecipe: this.isShowMoreRecipe,
            isShow: true
        };
    };

    IngredientModel.prototype.toDTO = function () {
        return {
            ingredientList: this.ingredientList,
            allergens: this.allergens,
            message: this.message || ''
        };
    };

    IngredientModel.prototype.makeSelectedIngredient = function (ingredient) {
        this.setSelectedIngredient(ingredient);
        return this.selectedIngredient;
    };

    IngredientModel.prototype.getMoreIngredient = function () {
        this.ingredientPage = this.ingredientPage + 1;
        return this.$http.get('/0/ingredients?filter=' + this.ingredientText + '&page=' + this.ingredientPage)
            .then(function (response) {
                var length = this.ingredients.list.length;
                this.ingredients.has_more = response.data.has_more;
                this.ingredients.total = response.data.total;
                this.ingredients.list = this.ingredients.list.concat(response.data.list);
                this.isShowMoreIngredient = this.ingredients.list.length !== length;
                return this.toDropdownDTO();
            }.bind(this));
    };

    IngredientModel.prototype.getMoreRecipe = function () {
        this.recipePage = this.recipePage + 1;
        return this.$http.get('/0/subrecipes?filter=' + this.ingredientText + '&page=' + this.recipePage)
            .then(function (response) {
                var length = this.recipes.list.length;
                this.recipes.has_more = response.data.has_more;
                this.recipes.total = response.data.total;
                this.recipes.list = this.recipes.list.concat(response.data.list);
                this.isShowMoreRecipe = this.recipes.list.length !== length;
                return this.toDropdownDTO();
            }.bind(this));
    };

    IngredientModel.prototype.validateAdding = function (context) {
        if (!this.selectedIngredient) {
            return this.handleIngredient(context);
        }
        else {
            var id = this.selectedIngredient.custom_id || this.selectedIngredient.generic_table_row_id;
            return id ? this.addIngredient(context) : this.addRecipe(context);
        }
    };

    IngredientModel.prototype.addIngredient = function (context) {
        var body = {
            costing_ingredient_id: this.selectedIngredient.custom_id || this.selectedIngredient.generic_table_row_id,
            is_custom: !!this.selectedIngredient.custom_id,
            text: context.amount
        };
        return this.$http.post('/0/recipes/' + RECIPE_ID + '/ingredient', body).then(function (response) {
            var ingredient = {
                id: response.data.id,
                name: context.amount + ' ' + response.data.name
            };
            this.setAllergens(response.data.allergens);
            this.setMessage(response.data.message || '');
            this.addIngredientToList(ingredient);
            return this.toDTO();
        }.bind(this));
    };


    IngredientModel.prototype.addRecipe = function (context) {
        var body = {
            recipe_id: RECIPE_ID,
            subrecipe_id: this.selectedIngredient.id,
            amount: context.amount || ''
        };
        return this.$http.post('/0/subrecipes', body).then(function (response) {
            var ingredient = {
                id: response.data.id,
                name: response.data.name,
                chef_name: response.data.owner_name
            };
            this.addIngredientToList(ingredient);
            return this.toDTO();
        }.bind(this));
    };

    IngredientModel.prototype.addIngredientToList = function (ingredient) {
        this.ingredientList.push(ingredient);
    };

    IngredientModel.prototype.validateDelete = function (ingredient) {
        return (ingredient.chef_name ? this.deleteRecipe(ingredient) : this.deleteIngredient(ingredient)).then(function () {
            this.removeIngredientFromList(ingredient);
            return this.toDTO();
        }.bind(this));
    };

    IngredientModel.prototype.deleteRecipe = function (recipe) {
        return this.$http.delete('/0/subrecipes?id=' + recipe.id);
    };

    IngredientModel.prototype.deleteIngredient = function (ingredient) {
        return this.$http.delete('/0/recipes/' + RECIPE_ID + '/ingredient?id=' + ingredient.id);
    };

    IngredientModel.prototype.removeIngredientFromList = function (ingredient) {
        this.ingredientList = this.ingredientList.filter(function (item) {
            return !(item.name === ingredient.name && item.id === ingredient.id);
        });
    };

    IngredientModel.prototype.clearSelectedIngredient = function () {
        this.selectedIngredient = false;
    };

    IngredientModel.prototype.checkIngredientsIsAlreadyExists = function (ingredient) {
        if (!this.ingredients.list || this.ingredients.list.length == 0)
            return false;
        for (var i = 0; i < this.ingredients.list.length; i++) {
            if (ingredient.toLowerCase().trim() == this.ingredients.list[i].ingredient.toLowerCase().trim()) {
                var id = this.ingredients.list[i].custom_id || this.ingredients.list[i].generic_table_row_id;
                this.selectedIngredient = this.ingredients.list[i];
                return id;
            }
        }
        return false;
    };

    IngredientModel.prototype.checkSubRecipeIsAlreadyExists = function (recipeName) {
        if (!this.recipes.list || this.recipes.list.length == 0)
            return false;
        for (var i = 0; i < this.recipes.list.length; i++) {
            if (recipeName.toLowerCase().trim() == this.recipes.list[i].name.toLowerCase().trim()) {
                var id = this.recipes.list[i].id;
                this.selectedIngredient = this.recipes.list[i];
                return id;
            }
        }

        return false;
    };

    IngredientModel.prototype.handleIngredient = function (context) {
        var id = this.checkIngredientsIsAlreadyExists(context.ingredient);
        if (id)
            return this.addIngredient(context);
        else {
            var subId = this.checkSubRecipeIsAlreadyExists(context.ingredient);
            if (subId)
                return this.addRecipe(context);
            return this.handleWithNewIngredient(context);
        }
        return {invalid: true, msg: 'ingredient not valid'}
    };

    IngredientModel.prototype.handleWithNewIngredient = function (context) {
        if (!this.isValidatingIngredient(context)) {
            return {invalid: true, msg: 'amount is required'};
        }
        var body = {
            costing_ingredient_id: this.capitalizedFirstLetter(context.ingredient),
            is_custom: true,
            text: context.amount
        };
        return this.$http.post('/0/recipes/' + RECIPE_ID + '/ingredient', body).then(function (response) {
            var ingredient = {
                id: response.data.id,
                name: context.amount + ' ' + response.data.name
            };
            this.setAllergens(response.data.allergens);
            this.setMessage(response.data.message || '');
            this.addIngredientToList(ingredient);
            return this.toDTO();
        }.bind(this));
    };

    IngredientModel.prototype.isValidatingIngredient = function (context) {
        if (!context.amount || context.amount.trim() == '')
            return false;
        return true;
    };

    IngredientModel.prototype.capitalizedFirstLetter = function (str) {
        str = str.trim();
        return str.charAt(0).toUpperCase() + str.slice(1);
    };

})(app, this);