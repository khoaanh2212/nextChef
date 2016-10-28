app.controller('RecipesListController', ['$scope', 'Recipe', function($scope, Recipe){
	$scope.currentFilterName = '';

    $scope.controlName = function(recipe) {
    	return recipe.getShortName();
    };

	$scope.loveRecipe = function(recipe){
		if(checkAuthenticated('love')){
			recipe.love().then(function(results){});
		}
    };
    
    $scope.commentRecipe = function(recipe){
		if(checkAuthenticated('comment')){
		}
    };
    
    $scope.addRecipe = function(recipe){
		if(checkAuthenticated('add')){
			
		}
    };
}]);