var app = angular.module('library', []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['Accept'] = 'application/json, text/javascript, */*; q=0.01';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
}]);

app.controller('LibraryController', ['$scope', 'Chef', function($scope, Chef){
	
	$scope.isUserAuthenticated = USER_AUTHENTICATED;
	$scope.userFollowsList = USER_FOLLOWS_LIST;
    $scope.userId = USER_ID;
	$scope.loadingAvatar = false;
	$scope.loadingRestaurant = false;
	$scope.loadingCover = false;
	$scope.restaurantActive = false;
    $scope.followersActive = false;
    $scope.followingActive = false;

    $scope.followersLoading = false;
    $scope.followingLoading = false;
	
	$scope.chef = new Chef({id: CHEF_ID});
    $scope.chef.checkFollowed($scope.userFollowsList);

	$scope.follow = function(chef){
		
		if(!$scope.isUserAuthenticated){
			checkAuthenticated('follow');
		}else{
			if(chef.followed){
				chef.follow().then(function(){
					chef.followed = false;
				});
			}else{
				chef.follow().then(function(){
					chef.followed = true;
				});
			}
		}
	};
	
	$scope.saveProfile = function(){
		 
		 var address = angular.element('#id_restaurant-address').val();
		 //var city = angular.element('#id_restaurant-city').val();
		 //var state = angular.element('#id_restaurant-state').val();
		 //var country = angular.element('#id_restaurant-country').val();
		 //var complete_address = address + ' ,' + city + ' ,' + state + ' ,' + country;
		 
		 var geocoder = new google.maps.Geocoder();
		 geocoder.geocode( { 'address': address}, function(results, status) {
			 if (status == google.maps.GeocoderStatus.OK) {
				 result = results[0];
				 for(var i=0; i<result.address_components.length; i++){
					 var component = result.address_components[i];
					 if(component.types.indexOf('country') != -1){
						 angular.element('#id_restaurant-country').val(component.long_name);
					 }else if(component.types.indexOf('postal_code') != -1){
						 angular.element('#id_restaurant-zip').val(component.long_name);
					 }else if(component.types.indexOf('administrative_area_level_1') != -1){
						 angular.element('#id_restaurant-state').val(component.long_name);
					 }else if(component.types.indexOf('locality') != -1){
						 angular.element('#id_restaurant-city').val(component.long_name);
					 }
				 }
				 angular.element('#id_restaurant-latitude').val(result.geometry.location.k);
				 angular.element('#id_restaurant-longitude').val(result.geometry.location.B);
				 
			 } else {
				 angular.element('#id_restaurant-latitude').val(0);
				 angular.element('#id_restaurant-longitude').val(0);
			 }
			 angular.element('#save_profile_form').submit();
		 });
		 
		 return false;
	 };
	 
	 $scope.setRestaurantMap = function(){
		 
		var map = document.getElementById('map_canvas');
		
		if(map != null){
			var geocoder = new google.maps.Geocoder();
			var latitude = RESTAURANT_LATITUDE;
			var longitude = RESTAURANT_LONGITUDE;
			
			if(latitude!='' && longitude!=''){
				var stylez = [{
					featureType: "all",
					elementType: "all",
					stylers: [{ saturation: -100 }]
				}];
				var latlng = new google.maps.LatLng(parseFloat(latitude), parseFloat(longitude));
				var mapOptions = { 
						zoom: 12, 
						center: latlng,
						panControl: false,
						zoomControl: true,
						scaleControl: false,
						streetViewControl: false,
						overviewMapControl: false,
						mapTypeControl: false
				};
				var map = new google.maps.Map(map, mapOptions);
				map.setOptions({styles: stylez});
				var marker = new google.maps.Marker({
					map: map,
				 	position: new google.maps.LatLng(parseFloat(latitude), parseFloat(longitude))
				});
			}
		}
	 };
	 
	 $scope.setRestaurantMap();
	 
	 $scope.uploadRestaurantImage = function(files){
		 $scope.loadingRestaurant = true;
		 $scope.chef.uploadRestaurantImage(files[0]).then(function(result){
			 if(result.data.success){
				 $('#library_modal_restaurant_image').attr('src', result.data.url);
			 }
			 $scope.loadingRestaurant = false;
		 });
	 };
	     
	 $scope.uploadAvatarImage = function(files){
    	 $scope.loadingAvatar = true;
      	 $scope.chef.uploadAvatarImage(files[0]).then(function(result){
      		if(result.data.success){
      			$('#library_modal_avatar').attr('src', result.data.url);
      		}
      		$scope.loadingAvatar = false;
      	 });
     };
     
     $scope.uploadCoverImage = function(files){
    	 $scope.loadingCover = true;
      	 $scope.chef.uploadCoverImage(files[0]).then(function(result){
      		if(result.data.success){
      			$('#library_modal_cover').attr('src', result.data.url);
      		}
      		$scope.loadingCover = false;
      	 });
     };

    $scope.showFollowers = function() {
        if ($scope.followersActive == false) {
            $scope.followingActive = false;
            $scope.followersActive = true;
            if ($scope.chef.followers == undefined) {
                $scope.followersLoading = true;
                $scope.chef.loadFollowers($scope.userFollowsList).then(function (result) {
                    $scope.followersLoading = false;
                });
            }
        }
        else {
            $scope.followersActive = false;
        }
    };

    $scope.showFollowing = function() {
        if ($scope.followingActive == false) {
            $scope.followersActive = false;
            $scope.followingActive = true;
            if ($scope.chef.following == undefined) {
                $scope.followingLoading = true;
                $scope.chef.loadFollowing($scope.userFollowsList).then(function (result) {
                    $scope.followingLoading = false;
                });
            }
        }
        else {
            $scope.followingActive = false;
        }
    }
}]);

app.factory('Chef', ['$http', function($http) {
	
	function Chef(chefData) {
        if (chefData) {
            this.setData(chefData);
        }
    };
    
    Chef.prototype = {
		followUrl: FOLLOW_URL,
		loadFollowingUrl: LOAD_FOLLOWING_URL,
		loadFollowersUrl: LOAD_FOLLOWERS_URL,
		uploadRestaurantImageUrl: UPLOAD_RESTAURANT_IMAGE_URL,
		uploadAvatarImageUrl: UPLOAD_AVATAR_IMAGE_URL,
		uploadCoverImageUrl: UPLOAD_COVER_IMAGE_URL,
        loadRecipesUrl: CHEF_RECIPES_URL,
		loadRecipesByNameUrl: CHEF_RECIPES_BY_NAME_URL,

		setData: function(chefData) {
            angular.extend(this, chefData);
        },
        checkFollowed: function(userList){
    		for (var i = 0; i < userList.length; i++) {
                if (userList[i] == this.id) {
                    this.followed = true;
                    return;
                }
            }
    		this.followed = false;
    	},
        setFollowing: function(followingData, chefsList) {
        	var following = [];
        	for(var i=0; i<followingData.length; i++){
        		var chef = new Chef(followingData[i]);
        		chef.checkFollowed(chefsList);
        		following.push(chef);
        	}
        	this.following = following;
        },
        setFollowers: function(followersData, chefsList) {
        	var followers = [];
        	for(var i=0; i<followersData.length; i++){
        		var chef = new Chef(followersData[i]);
        		chef.checkFollowed(chefsList);
        		followers.push(chef);
        	}
        	this.followers = followers;
        },
        follow: function() {
        	var scope = this;
        	return $http.post(this.followUrl, $.param({chef_id: this.id})).success(function(follower_data) {
        		//scope.setData(followData.follower_data);
        	});
        },
        loadFollowing: function(chefsList){
        	var scope = this;
            return $http.get(this.loadFollowingUrl.replace('CHEF_ID', this.id)).success(function (results) {
                scope.setFollowing(results.following, chefsList);
            });
        },
        loadFollowers: function(chefsList){
        	var scope = this;
            return $http.get(this.loadFollowersUrl.replace('CHEF_ID', this.id)).success(function (results) {
                scope.setFollowers(results.followers, chefsList);
            });
        },
        uploadRestaurantImage: function(file){
        	var fd = new FormData();
            fd.append('image', file);
        	return $http.post(this.uploadRestaurantImageUrl.replace('CHEF_ID', this.id), fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
        },
        uploadAvatarImage: function(file){
        	var fd = new FormData();
            fd.append('image', file);
        	return $http.post(this.uploadAvatarImageUrl.replace('CHEF_ID', this.id), fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
        },
        uploadCoverImage: function(file){
        	var fd = new FormData();
            fd.append('image', file);
        	return $http.post(this.uploadCoverImageUrl.replace('CHEF_ID', this.id), fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
        },
        loadRecipes: function(page){
        	var scope = this;
        	return $http.get(this.loadRecipesUrl.replace('CHEF_ID', this.id) + '?page=' + page);
        },
		loadRecipesByName: function(name, page){
        	var scope = this;
			var urlAfter = this.loadRecipesByNameUrl.replace('CHEF_ID', this.id);
			urlAfter = urlAfter.replace('NAME', name);
        	return $http.get(urlAfter + '?page=' + page);
        }
    };
    return Chef;
}]);

app.controller('BooksController', ['$scope', 'Book', 'Recipe', 'Chef', function($scope, Book, Recipe, Chef){
	
	$scope.loadingRecipes = false;
	$scope.books = [];
	$scope.chefId = CHEF_ID;
	$scope.chefRecipes = [];
	$scope.chefRecipesCount = 0;
	$scope.currentChefRecipesPage = 1;
    $scope.bookRecipesCount = 0;
    $scope.bookRecipesTotal = 0;
	$scope.drafts = DRAFTS;
	$scope.userLovesList = USER_LOVES_LIST;
	$scope.currentBookId = [];
	$scope.currentRecipes = [];
	$scope.loadingMore = false;
    $scope.currentBook;
	
	$scope.newBookName = '';
	$scope.bookToEdit = null;
	$scope.bookToEditOldName = '';
	$scope.bookToDelete = null;

	for(var i=0; i<BOOKS.length; i++){
		var book = new Book(BOOKS[i]);
		$scope.books.push(book);
	}
	
	$scope.commentsLine = function(recipe, number){
		return recipe.last_comments.length == number;
	};
	
	$scope.setBookToEdit = function(book){
		$scope.bookToEdit = book;
		$scope.bookToEditOldName = book.name;
	};
	
	$scope.setBookToDelete = function(book){
		$scope.bookToDelete = book;
	};

	$scope.showChefRecipes = function(){
        if ($scope.chefRecipes.length == 0) {
            //$scope.loadingRecipes = true;
            var chef = new Chef({
                id: $scope.chefId
            });
            
            chef.loadRecipes($scope.currentChefRecipesPage).then(function(recipesArray){
                $scope.currentRecipes = [];
                $scope.chefRecipes = [];
                $scope.chefRecipesCount = recipesArray.data.count;
				for(var i=0; i<recipesArray.data.results.length; i++){
                    var recipe = new Recipe(recipesArray.data.results[i]);
                    recipe.checkLoved($scope.userLovesList);
                    $scope.chefRecipes.push(recipe);
	        	}
				$scope.currentChefRecipesPage++;
				$scope.currentRecipes = $scope.chefRecipes;
                $scope.currentBookId = 'chefRecipes';
				$scope.loadingRecipes = false;
            })
        } else {
            $scope.currentRecipes = $scope.chefRecipes;
		    $scope.currentBookId = 'chefRecipes';
        }
        window.location.hash = '#recipes';
	};
	
	$scope.loadMoreChefRecipes = function(){
        var chef = new Chef({
            id: $scope.chefId
        });
        $scope.loadingMore = true;
        chef.loadRecipes($scope.currentChefRecipesPage).then(function(recipesArray){
			for(var i=0; i<recipesArray.data.results.length; i++){
                var recipe = new Recipe(recipesArray.data.results[i]);
                recipe.checkLoved($scope.userLovesList);
                $scope.chefRecipes.push(recipe);
        	}
			$scope.currentChefRecipesPage++;
			$scope.loadingMore = false;
        })
	};
	
	$scope.showDrafts = function(){
        $scope.loadingRecipes = true;
		$scope.currentRecipes = $scope.drafts;
		$scope.currentBookId = 'drafts';
		$scope.loadingRecipes = false;
        window.location.hash = '#drafts';
	};
	
	$scope.showBookRecipes = function(book){
		$scope.loadingRecipes = true;
		$scope.currentBookId = book.id;
        $scope.currentBook = book;
		if(book.recipes == undefined){
            book.setPage(1);
			book.loadRecipes().then(function(recipesArray){
                book.setTotalRecipes(recipesArray.data.count);
                $scope.bookRecipesTotal = book.TotalRecipes;
				$scope.currentRecipes = [];
				for(var i=0; i<book.recipes.length; i++){
                    book.recipes[i].checkLoved($scope.userLovesList);
	        	}
                $scope.bookRecipesCount = book.recipes.length;
				$scope.currentRecipes = book.recipes;
				$scope.loadingRecipes = false;
			});
		}else{
			$scope.currentRecipes = book.recipes;
            $scope.bookRecipesTotal = book.TotalRecipes;
            $scope.bookRecipesCount = book.recipes.length;
			$scope.loadingRecipes = false;
		}
        window.location.hash = '#'+slug(book.name)+'-'+book.id;
	};

    $scope.loadMoreBookRecipes = function(){
        $scope.loadingMore = true;
        $scope.currentBook.loadRecipes().then(function(recipesArray){
            $scope.currentRecipes = [];
            for(var i=0; i<$scope.currentBook.recipes.length; i++){
                $scope.currentBook.recipes[i].checkLoved($scope.userLovesList);
            }
            $scope.currentRecipes = $scope.currentBook.recipes;
            $scope.bookRecipesCount = $scope.currentBook.recipes.length;
            $scope.loadingMore = false;
		});
	};
	
	$scope.addNewBook = function(newBookName){
		var book = new Book();
		book.create(newBookName).then(function(response){
			$scope.books.push(book);
			$scope.newBookName = '';
		});
	};
	
	$scope.editBook = function(book){
		book.edit().then(function(response){
			$scope.bookToEdit = null;
		});
	};
	
	$scope.deleteBook = function(book){
		book.delete().then(function(response){
			var index = $scope.books.indexOf(book)
			$scope.books.splice(index, 1); 
			$scope.bookToDelete = null;
		});
	};

    $scope.init = function() {
        var hash = window.location.hash;
        if (hash == '#drafts') {
            $scope.showDrafts();
        }
        else if (hash == '#recipes') {
            $scope.showChefRecipes();
        }
        else if (hash != '') {
            var splitted = hash.split('-');
            for(var i=0; i<$scope.books.length; i++) {
                if ($scope.books[i].id == splitted[1]) {
                    $scope.showBookRecipes($scope.books[i]);
                    break;
                }
            }
        }
        else $scope.showChefRecipes();
    };


    $scope.init();

}]);


app.controller('RecipesController', ['$scope', 'Recipe', function($scope, Recipe){
	$scope.currentFilterName = '';
	
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

app.factory('Book', ['$http', 'Recipe', function($http, Recipe) {
	
	function Book(bookData) {
        if (bookData) {
            this.setData(bookData);
        }
    };
    
    Book.prototype = {
		addBookUrl: ADD_BOOK_URL,
		editBookUrl: EDIT_BOOK_URL,
		deleteBookUrl: DELETE_BOOK_URL,
		loadRecipesUrl: LOAD_RECIPES_URL,
		setData: function(bookData) {
            angular.extend(this, bookData);
        },
        setRecipes: function(recipesArray) {
            for (var i = 0; i < recipesArray.length; i++) {
                this.recipes.push(new Recipe(recipesArray[i]));
            }
        },
        create: function(bookName) {
        	this.name = bookName;
        	var scope = this;
        	return $http.post(this.addBookUrl, $.param({name:this.name})).success(function(bookData) {
        		scope.setData(bookData.book_data);
        	});

        },
        delete: function(){
        	var scope = this;
        	return $http.post(this.deleteBookUrl.replace('BOOK_ID', this.id)).success(function(result) {
        		
        	});
        },
        edit: function(){
        	var scope = this;
        	return $http.post(this.editBookUrl.replace('BOOK_ID', this.id), $.param({name:this.name})).success(function(result) {
        		
        	});
        },
        loadRecipes: function() {
        	var scope = this;
        	return $http.get(this.loadRecipesUrl.replace('BOOK_ID', this.id) + '?page=' + scope.page).success(function(recipes) {
        		scope.setRecipes(recipes.results);
                scope.page++;
        	});
        },
        setTotalRecipes: function(length) {
            var scope = this;
            scope.TotalRecipes = length;
        },
        setPage: function(value) {
            var scope = this;
            scope.page=value;
            scope.recipes = [];
        }
    };
    return Book;
}]);

app.filter('chefFilter', function() {
	return function(data, chef_id, different) {
		var filtered = [];
	    if (different == 0) {
	    	return data;
	    }else{
	    	for (var i=0;i<data.length;i++) {
	    		var value = data[i];
	    		if (different<0 && value.chef_id == chef_id || different>0 && value.chef_id != chef_id) {
	    			filtered.push(value);
	    		}
	    	}
	    }
	    return filtered;
	  }
	});

app.factory('Recipe', ['$http', function($http) {
	
	function Recipe(recipeData) {
		this.loved = false;
        if (recipeData) {
            this.setData(recipeData);
        }
    };
    
    Recipe.prototype = {
		loveRecipeUrl: LOVE_RECIPE_URL,
		setData: function(recipeData) {
            angular.extend(this, recipeData);
        },
        checkLoved: function(lovedRecipes){
        	this.loved = lovedRecipes.indexOf(this.id) != -1;
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
        }
    };
    return Recipe;
}]);


function initAffix(){

    var fixed = false;
    var absolute = false;
    $('.affix-sidebar').height($(window).height());
    $('.affix-main').css('min-height', $(window).height());
    
    function checkAffix(){
    	
    	var underHeader = $(window).scrollTop() > ($('.navbar-inverse').outerHeight() + $('#library_controller').outerHeight() +
            15 + $('.followers').outerHeight() + $('.following').outerHeight());
        var underFooter = $(window).scrollTop() + $(window).height() > $('#footer').offset().top;
        
        if(!underHeader && !fixed){ //top
            $('.chef-data').removeClass('active');
            $('.affix-sidebar').removeClass('cb-affix');
            $('.affix-sidebar').removeClass('cb-affix-bottom');
            $('.affix-sidebar').height($(window).height());
            $('.affix-sidebar').find('.scrollable-list').height($(window).height());
            $('.affix-main').css('margin-left', 0);
            absolute = false;
        }
        if(!underHeader && fixed){ //top
            $('.chef-data').removeClass('active');
            $('.affix-sidebar').removeClass('cb-affix');
            $('.affix-sidebar').removeClass('cb-affix-bottom');
            $('.affix-sidebar').height($(window).height());
            $('.affix-sidebar').find('.scrollable-list').height($(window).height() - 100);
            $('.affix-main').css('margin-left', 0);
            fixed = false;
            absolute = false;
        }
        if(underHeader && !underFooter && !fixed){ //fixed
            fixed = true;
            absolute = false;
            $('.chef-data').addClass('active');
            $('.affix-sidebar').addClass('cb-affix');
            $('.affix-sidebar').removeClass('cb-affix-bottom');
            $('.affix-main').css('margin-left', $('.affix-sidebar').css('width'));
            $('.affix-sidebar').height($(window).height());
            $('.affix-sidebar').find('.scrollable-list').height($(window).height() - 100);
        }
        if(underHeader && underFooter){ //bottom
            fixed = false;
            absolute = true;
            $('.affix-sidebar').removeClass('cb-affix');
            $('.affix-sidebar').addClass('cb-affix-bottom');
            $('.affix-sidebar').height($(window).height());
            $('.affix-sidebar').find('.scrollable-list').height($(window).height() - $('.chef-data').height());
            $('.affix-main').css('margin-left', $('.affix-sidebar').css('width'));
        }
    }
    
    $(window).scroll(function(){
    	checkAffix();
    }).resize(function(){
        $('.affix-sidebar').height($(window).height());
        $('.affix-main').css('min-height', $(window).height());
        if (fixed || absolute) {
            $('.chef-data').css('width', $('.affix-sidebar').width())
            $('.affix-main').css('margin-left', $('.affix-sidebar').css('width'));
            $('.affix-sidebar').find('.scrollable-list').height($(window).height() - 100);
        }
        
    });
    
    checkAffix();
};

$(document).ready(function(){
	
	$('#upload_avatar_image_button').click(function(){
		$('#upload_avatar_image_input').click();
	});
	
	$('#upload_avatar_image_input').change(function(evt){
		var scope = angular.element(document.getElementById('library_controller')).scope();
		scope.uploadAvatarImage(evt.target.files);	
	});
	
	$('#upload_cover_image_button').click(function(){
		$('#upload_cover_image_input').click();
	});
	
	$('#upload_cover_image_input').change(function(evt){
		var scope = angular.element(document.getElementById('library_controller')).scope();
		scope.uploadCoverImage(evt.target.files);	
	});
	
	$('#upload_restaurant_image_button').click(function(){
		$('#upload_restaurant_image_input').click();
	});
	
	$('#upload_restaurant_image_input').change(function(evt){
		var scope = angular.element(document.getElementById('library_controller')).scope();
		scope.uploadRestaurantImage(evt.target.files);	
	});
    initAffix();
});