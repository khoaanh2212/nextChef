(function() {
	
	app.controller("NewUserExperienceController", ['$scope', function ($scope) {
		$scope.showChefs = false;
		$scope.is_foodie = true;
		$scope.chef_ids = [];
		
		$scope.selectChefOrFoodie = function(foodie){
			$scope.is_foodie = foodie;
			$scope.showChefs = true;
		};
		
		$scope.isChefSelected = function(chefId){
			for(var i=0; i<$scope.chef_ids.length; i++){
				if($scope.chef_ids[i] == chefId){
					return true;
				}
			}
			return false;
		};
		
		$scope.selectChefId = function(chefId){
			var found = false;
			for(var i=0; i<$scope.chef_ids.length; i++){
				if($scope.chef_ids[i] == chefId){
					$scope.chef_ids.splice(i, 1);
					found = true;
				}
			}
			if(!found){
				$scope.chef_ids.push(chefId);
			}
		};
		
		$scope.finishNux = function(){
			$('#nuxform_type').val($scope.is_foodie);
			$('#nuxform_chefs').val($scope.chef_ids);
			$('#nuxform').submit();
		};
		
	}]);
	
}).call(this);

