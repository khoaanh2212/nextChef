
function activeLoader(){
	$('.load-more button').fadeOut(300, function(){
		$('.load-more .loader').fadeIn(300);
	});
}

function deactivateLoader(){
	$('.load-more .loader').fadeOut(300, function(){
		$('.load-more button').fadeIn(300);
	});
}

(function() {
	
	var App = angular.module('cookbooth.chefs.app', []);

	App.controller("ChefsController", ['$scope','ChefsService', function ($scope, ChefsService) {
		$scope.chefs = [];
	    $scope.chefsSrc = MORE_CHEFS_URL + "?page=2";
	    $scope.loadChefs = function(){    
	    	activeLoader();
	    	ChefsService.parseChefs($scope.chefsSrc).then(function(res){
	    		$scope.chefsSrc = res.data.next;
	    		deactivateLoader();
	            return angular.forEach(res.data.results, function(item) {
	    			return $scope.chefs.push(item);
	    		});
	        });
	    }
        $scope.do_follow = function(chef_id){
        	follows_do_follow(chef_id);
	    }
        $scope.is_following = function(chef_id){
            if(user_is_authenticated) {
                for (var i = 0; i < follows_list.length; i++) {
                    if (follows_list[i] == chef_id)
                        return true;
                }
                return false;
            }else{
                return false;
            }
	    }
	}]);

	App.factory('ChefsService',['$http',function($http){
	    return {
	    	parseChefs : function(url){
	            return $http.get(url);
	        }
	    }
	}]);
	
}).call(this);
