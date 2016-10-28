(function() {
	
	app.controller("CollectionController", ['$scope','Recipe', function ($scope, Recipe) {
		$scope.recipes = [];
		$scope.userLovesList = USER_LOVED_RECIPES;
		
		$scope.initRecipes = function(){     
	    	for(var i=0; i<INIT_RECIPES.length; i++){
	            var recipe = new Recipe(INIT_RECIPES[i]);
	            recipe.checkLoved($scope.userLovesList);
	            $scope.recipes.push(recipe);
	    	}
	    }
	    $scope.initRecipes();
	}]);
	
}).call(this);

