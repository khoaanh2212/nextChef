(function() {
	
	app.controller("BookController", ['$scope', '$sce','Recipe', function ($scope, $sce, Recipe) {
		$scope.recipes = [];
		$scope.userLovesList = USER_LOVED_RECIPES;
		$scope.stripe_key;
		$scope.need_login = NEED_LOGIN;
		$scope.need_change_password = NEED_CHANGE_PASSWORD;
		$scope.buy_callback_modal = BUY_CALLBACK_MODAL;
		$scope.already_bought = ALREADY_BOGUTH;
		$scope.recipe_popup;
		$scope.login_before_buy=false;
		
		$scope.init = function(){
			$scope.initRecipes();
			
			if($scope.buy_callback_modal)
				$('#buy_callback_modal').modal('show');
			
			if($scope.already_bought)
				$('#already_bought_modal').modal('show');
			
			if(getCookie('book_' + BOOK_ID) == null){
				setCookie('book_' + BOOK_ID, true, 365);
				$scope.showBookVideo();
			}

		};
		
		$scope.showBookVideo = function(){
			var modal = $('#video_modal');
			modal.modal('show');
			modal.find('video')[0].play();
		};
		
		$scope.hideBookVideo = function(){
			var modal = $('#video_modal');
			modal.modal('hide');
			modal.find('video')[0].pause();
		};
		
		$scope.initRecipes = function(){     
	    	for(var i=0; i<INIT_RECIPES.length; i++){
	            var recipe = new Recipe(INIT_RECIPES[i]);
	            recipe.checkLoved($scope.userLovesList);
	            $scope.recipes.push(recipe);
	    	}
	    };
	    
	    $scope.showBuyForm = function(name, description, label, price, image){
	    	$('#buy_book_modal').modal('hide');
	        var handler = StripeCheckout.configure({
	            key: $scope.stripe_key,
	            image: image,
	            name: name,
	            description: description,
	            panelLabel: label,
	            allowRememberMe: false,
	            token: function(token) {
	                $form = $("#checkout_form");
	                $form.find("input[name=stripe_token]").val(token.id);
	                $form.find("input[name=stripe_response]").val(JSON.stringify(token));
	                $form.trigger("submit");
	            }
	        });
	        handler.open();
	    };
	    
	    $scope.gotoRecipe = function(recipe){
	    	$scope.login_before_buy=false;
	    	var modal = $('#buy_book_modal');
	    	if(modal.length == 0){
	    		document.location.href = recipe.url;
	    	}else{
		    	$scope.recipe_popup = recipe;
		    	$scope.html_description = $sce.trustAsHtml($scope.recipe_popup.description);
		    	$scope.$apply();
				dialog = modal.find('.modal-dialog');
		        modal.css('display', 'block');
		        dialog.css("margin-top", Math.max(0, ($(window).height() - dialog.height()) / 2));
				modal.modal('show');
	    	}
	    };
	    
	    $scope.showBuyPopup = function(){
	    	$scope.login_before_buy=false;
	    	var modal = $('#buy_book_modal');
	    	$scope.recipe_popup = null;
	    	$scope.$apply();
			dialog = modal.find('.modal-dialog');
	        modal.css('display', 'block');
	        dialog.css("margin-top", Math.max(0, ($(window).height() - dialog.height()) / 2));
			modal.modal('show');
	    };
	    
	    $scope.showLoginBeforeBuyPopup = function(){
	    	$scope.login_before_buy=true;
	    	$scope.$apply();
	    	var modal = $('#buy_book_modal');
	    	dialog = modal.find('.modal-dialog');
	        modal.css('display', 'block');
	        dialog.css("margin-top", Math.max(0, ($(window).height() - dialog.height()) / 2));
	    };
	    
	    $scope.init();
	    
	}]);
	
}).call(this);

