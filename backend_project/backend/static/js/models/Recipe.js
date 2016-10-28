
app.factory('Recipe', ['$http', '$filter', 'Step', function($http, $filter, Step) {

    function Recipe(recipeData) {
    	this.loved = false;
    	this.stepsLoaded = false;
    	this.steps = [];

    	try {
            this.loadRecipeUrl= GET_RECIPE_URL;
        }catch(err) { }
        try {
            this.getIngredientsSuggestionUrl= GET_INGREDIENTSSUGGESTION_URL;
        }catch(err) { }
        try {
            this.editIngredientsUrl= EDIT_INGREDIENTS_URL;
        }catch(err) { }
        try {
            this.editTagsUrl= EDIT_TAGS_URL;
        }catch(err) { }
        try {
            this.editAllergenUrl= EDIT_ALLERGEN_URL;
        }catch(err) { }
        try {
            this.editTitleUrl= EDIT_TITLE_URL;
        }catch(err) { }
        try {
            this.editServesUrl= EDIT_SERVES_URL;
        }catch(err) { }
        try {
            this.editPrepTimeUrl= EDIT_PREP_TIME_URL;
        }catch(err) { }
        try {
            this.selectBookUrl= SELECT_BOOK_URL;
        }catch(err) { }
        try {
            this.publishUrl= PUBLISH_RECIPE_URL;
        }catch(err) { }
        try {
            this.makePrivateUrl= MAKE_PRIVATE_RECIPE_URL;
        }catch(err) { }
        try {
            this.loveRecipeUrl= RECIPE_LOVE_URL;
        }catch(err) { }
        try {
            this.deleteRecipeUrl = RECIPE_DELETE_URL;
        }catch(err) { }

        if (recipeData) {
            this.setData(recipeData);
        }
    };

    Recipe.prototype = {

        setData: function(recipeData) {
            angular.extend(this, recipeData);

            if(!this.stepsLoaded && recipeData.photos){
                for(var i=0; i<recipeData.photos.length; i++){
                    this.steps.push(new Step(recipeData.photos[i]));
                }
                this.stepsLoaded = true;
                if(document.location.pathname == '/kitchen/'){
                	this.name = '';
                }
            }

            /*
            this.xmasClass = this.getRandomXmasClass();

            if(this.tags != undefined){
                var string = "";
            	this.has_christmas_tag = false;
            	for(var i=0; i<this.tags.length; i++){
                    string = this.tags[i].name.toLowerCase();
            		if(string.indexOf('christmas') != -1){
            			this.has_christmas_tag = true;
            		}
                    else if(string.indexOf('christmas') != -1){
            			this.has_christmas_tag = true;
            		}
                    else if(string.indexOf('xmas') != -1){
            			this.has_christmas_tag = true;
            		}
                    else if(string.indexOf('navidad') != -1){
            			this.has_christmas_tag = true;
            		}
                    else if(string.indexOf('nadal') != -1){
            			this.has_christmas_tag = true;
            		}
                    else if(string.indexOf('xmasday') != -1){
            			this.has_christmas_tag = true;
            		}
            	}
            }*/
        },
        loadRecipe: function() {
            var scope = this;
            return $http.get(this.loadRecipeUrl.replace('RECIPE_ID', this.id)).success(function(recipeData) {
                if(recipeData.success){
                    scope.setData(recipeData.recipe);
                    //scope.hours = parseInt(recipeData.recipe.prep_time / 60);
                    //scope.minutes = recipeData.recipe.prep_time % 60;
                }
            });
        },
        checkLoved: function(lovedRecipes){
        	this.loved = lovedRecipes.indexOf(this.id) != -1;
        },
        getRandomXmasClass: function(){
    		return 'xmas-icon-' + String(Math.floor( Math.random() * 5 ) + 1);
    	},
        love: function() {
        	var scope = this;

        	if(!scope.loved){
        		scope.loved = true;
        		scope.nb_likes = parseInt(scope.nb_likes) + 1;
			}else{
				scope.loved = false;
				value = parseInt(scope.nb_likes);
				if(value != 0){
					scope.nb_likes = value - 1;
				}
			}

        	return $http.post(this.loveRecipeUrl.replace('RECIPE_ID', this.id)).success(function(recipeData) {
        		if(!recipeData.success){
        			if(!scope.loved){
        				scope.loved = true;
        				scope.nb_likes = parseInt(scope.nb_likes) + 1;
        			}else{
        				value = parseInt(scope.nb_likes);
        				if(value != 0){
        					scope.nb_likes = value - 1;
        				}
        				scope.loved = false;
        			}
        		}
        	});
        },
        addStep: function(step){
        	this.steps.push(step);
        },
        getCover: function(){
        	for(var i=0; i<this.steps.length; i++){
        		if(this.steps[i].cover){
        			return this.steps[i];
        		}
        	}
        	return null;
        },
        selectCover: function(step){
        	for(var i=0; i<this.steps.length; i++){
        		this.steps[i].cover = false;
        	}
            step.selectAsCover();
        },
        editTitle: function(){
        	this.public_url = 'nextchef.co/recipe/' + slug(this.name)  + '-' + this.id;
        	return $http.post(this.editTitleUrl.replace('RECIPE_ID', this.id), $.param({'title':this.name}));
        },
        editServes: function(){
        	return $http.post(this.editServesUrl.replace('RECIPE_ID', this.id), $.param({'serves':this.serves}));
        },
        editPrepTime: function(){
        	//var minutes = this.hours * 60 + this.minutes;
        	return $http.post(this.editPrepTimeUrl.replace('RECIPE_ID', this.id), $.param({'minutes':this.prep_time}));
        },
        selectBook: function(bookId){
            var index = this.books_ids.indexOf(bookId);
            if( index != -1){
                this.books_ids.splice(index, 1);
                return $http.post(this.selectBookUrl.replace('RECIPE_ID', this.id), $.param({'book_id':bookId, 'selected': false}));
            }else{
                this.books_ids.push(bookId);
                return $http.post(this.selectBookUrl.replace('RECIPE_ID', this.id), $.param({'book_id':bookId, 'selected': true}));
            }

        	return $http.post(this.selectBookUrl.replace('RECIPE_ID', this.id), $.param({'book_id':bookId, 'selected': selected}));
        },
        getIngredientsSuggestion: function(searchKey, successCallback){
            return $http.get(this.getIngredientsSuggestionUrl.replace('SEARCH_KEY', searchKey)).success(function(ingredientData) {
                if(ingredientData.success){
                    successCallback (ingredientData.ingredient);
                }
            });
        },
        editIngredients: function(){
        	return $http.post(this.editIngredientsUrl.replace('RECIPE_ID', this.id), $.param({'ingredients':JSON.stringify(this.ingredients)}));
        },
        editTags: function(){
        	return $http.post(this.editTagsUrl.replace('RECIPE_ID', this.id), $.param({'tags':JSON.stringify(this.tags)}));
        },

        editAllergen: function(){
            var data = {
                "added_allergens": JSON.stringify(this.added_allergens),
                "deleted_allergens": JSON.stringify(this.deleted_allergens)
            };
            return $http.post(this.editAllergenUrl.replace('RECIPE_ID', this.id), $.param(data));
        },
        deleteStep: function(step) {
            step.deleteStep();
            var isCover = step.cover;
            var index = this.steps.indexOf(step);
            this.steps.splice(index, 1);
            var orderBy = $filter('orderBy');
            var orderedSteps = orderBy(this.steps, 'order', false);
            for(var i=0; i<orderedSteps.length; i++){
            	if(i==0 && isCover){
            		this.selectCover(orderedSteps[i]);
            	}
                orderedSteps[i].order = i + 1;
            }
        },
        publish: function(){
        	this.public_url = '/recipe/' + slug(this.name)  + '-' + this.id;
        	this.isPrivate = false;
        	return $http.post(this.publishUrl.replace('RECIPE_ID', this.id));
        },
        makePrivate: function(){
        	this.public_url = '/recipe/' + slug(this.name)  + '-' + this.id;
        	this.isPrivate = true;
        	return $http.post(this.makePrivateUrl.replace('RECIPE_ID', this.id));
        },
        deleteRecipe: function(){
            return $http.post(this.deleteRecipeUrl.replace('RECIPE_ID', this.id));
        },
        getShortName: function(){
        	if (typeof this.name != 'undefined' && this.name != null){
        		try{
	        		var text = this.name;
	                if (text.length > 65) {
                        text = text.substring(0, 65);
                        text = text + "...";
                        return text;
                    }
	                else return text;
        		}catch(Exception){

        		}
        	}
        }
    };
    return Recipe;
}]);
