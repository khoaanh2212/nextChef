(function() {
	
	app.controller("SearchController", ['$scope','Recipe','RecipesService', function ($scope, Recipe, RecipesService) {
		$scope.recipes = [];
		$scope.loading = false;
		$scope.currentPage = 1;
        try {
            $scope.userLovesList = USER_LOVES_LIST;
        }catch(err) { }
		try {
            $scope.recipesSrc = SEARCH_LIST_RECIPES_URL;
        }catch(err) { }

		$scope.searchQuery = KEYWORDS;
		
		$scope.initRecipes = function(){     
	    	for(var i=0; i<INIT_RECIPES.length; i++){
	            var recipe = new Recipe(INIT_RECIPES[i]);
	            recipe.checkLoved($scope.userLovesList);
	            $scope.recipes.push(recipe);
	    	}
	    };
        $scope.initRecipes();
	    
	    $scope.loadRecipes = function(){     
	    	$scope.loading = true;
	    	
	    	RecipesService.getRecipes($scope.searchQuery, $scope.currentPage + 1).then(function(response){
	    		$scope.recipesSrc = response.data.next;
	    		$scope.currentPage = $scope.currentPage + 1;
	    		
	    		for(var i=0; i<response.data.results.length; i++){
		            var recipe = new Recipe(response.data.results[i]);
		            recipe.checkLoved($scope.userLovesList);
		            $scope.recipes.push(recipe);
		    	}
	    		
				var stateDataObj = { 	
					recipes: $scope.recipes, 
					next_url: $scope.recipesSrc
				};
	            history.pushState(stateDataObj, '', document.location.href);
	            
	            $scope.loading = false;
				return response
	        });
	    }

	}]);

	app.factory('RecipesService',['$http',function($http){
		return {
			listRecipesUrl: SEARCH_LIST_RECIPES_URL,
	    	getRecipes: function(query,page){
	            return $http.get(this.listRecipesUrl + "?" + $.param({q:query, page: page}));
	        },
	    }
	}]);
	
}).call(this);

window.addEventListener("popstate", function(e) {
	var state = e.state;
	scope = angular.element(document.getElementById('explore')).scope();
	scope.recipes = e.state.recipes;
	scope.recipesSrc = e.state.next_url;
	scope.$apply();
});