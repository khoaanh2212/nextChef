(function () {

    app.controller("ExploreController", ['$scope', 'Recipe', 'Chef', 'RecomendedService', 'FollowingService', function ($scope, Recipe, Chef, RecomendedService, FollowingService) {

        $scope.RECIPE = 0;
        $scope.NOTED = 5;
        $scope.BANNER = 1;
        $scope.CHEF = 2;
        $scope.BOOK = 3;
        $scope.COLLECTION = 4;

        $scope.loading = false;
        $scope.exploreItems = [];
        $scope.nextRecomendedPage = 2;
        $scope.nextFollowingPage = 2;
        $scope.userLovesList = USER_LOVED_RECIPES;
        $scope.order = [3, 0, 0, 2, 0, 5, 0, 0, 4, 0, 5, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        $scope.section = SECTION;

        // ADD NEW CONTENT DEPENDING THE ORDER
        $scope.addMore = function (response) {
            var recipesCounter = 0;
            var chefsCounter = 0;
            var booksCounter = 0;
            var bannersCounter = 0;
            var notedCounter = 0;
            var collsCounter = 0;

            if ($scope.section == 'RECOMMENDED') {
                for (var i = 0; i < $scope.order.length; i++) {
                    // CHEF
                    if (typeof response.chefs != 'undefined' && chefsCounter < response.chefs.length && $scope.order[i] == $scope.CHEF) {
                        var chef = new Chef(response.chefs[chefsCounter]);
                        chefsCounter++;
                        chef.itemType = $scope.CHEF;
                        $scope.exploreItems.push(chef);

                        // BANNER
                    } else if (typeof response.banners != 'undefined' && bannersCounter < response.banners.length && $scope.order[i] == $scope.BANNER) {
                        var tmp = response.banners[bannersCounter];
                        bannersCounter++;
                        tmp.itemType = $scope.BANNER;
                        $scope.exploreItems.push(tmp);

                        // COLLECTION
                    } else if (typeof response.colls != 'undefined' && collsCounter < response.colls.length && $scope.order[i] == $scope.COLLECTION) {
                        var tmp = response.colls[collsCounter];
                        collsCounter++;
                        tmp.itemType = $scope.COLLECTION;
                        $scope.exploreItems.push(tmp);

                        // BOOK
                    } else if (typeof response.books != 'undefined' && booksCounter < response.books.length && $scope.order[i] == $scope.BOOK) {
                        var tmp = response.books[booksCounter];
                        booksCounter++;
                        tmp.itemType = $scope.BOOK;
                        $scope.exploreItems.push(tmp);

                        // NOTED RECIPE
                    } else if (typeof response.noted != 'undefined' && notedCounter < response.noted.length && $scope.order[i] == $scope.NOTED) {
                        var recipe = new Recipe(response.noted[notedCounter]);
                        notedCounter++;
                        recipe.itemType = $scope.RECIPE;
                        recipe.checkLoved($scope.userLovesList);
                        $scope.exploreItems.push(recipe);

                    }
                    // RECIPE
                    // else if (typeof response.recipes != 'undefined' && recipesCounter < response.recipes.length
                    // /*&& $scope.order[i] == $scope.RECIPE*/) {
                    //     var recipe = new Recipe(response.recipes[recipesCounter]);
                    //     recipesCounter++;
                    //     recipe.itemType = $scope.RECIPE;
                    //     recipe.checkLoved($scope.userLovesList);
                    //     $scope.exploreItems.push(recipe);
                    // }
                }

            } else if ($scope.section == 'FOLLOWING') {
                // for (var i = 0; i < response.recipes.length; i++) {
                //     var recipe = new Recipe(response.recipes[i]);
                //     recipe.itemType = $scope.RECIPE;
                //     recipe.checkLoved($scope.userLovesList);
                //     $scope.exploreItems.push(recipe);
                // }
            }

            // SAVING THE STATUS FOR THE BROWSER BACK BUTTON
            var stateDataObj = {
                exploreItems: $scope.exploreItems,
                nextRecomendedPage: $scope.nextRecomendedPage,
            };
            history.pushState(stateDataObj, '', document.location.href);

            $scope.loading = false;
        };

        // GET NEW CONTENT FRON THE API
        $scope.loadMore = function () {
            if (!$scope.loading) {
                $scope.loading = true;
                if ($scope.section == 'RECOMMENDED') {
                    RecomendedService.getRecipes($scope.nextRecomendedPage).then(function (response) {
                        $scope.nextRecomendedPage++;
                        $scope.addMore(response.data)
                    });
                } else if ($scope.section == 'FOLLOWING') {
                    FollowingService.getRecipes($scope.nextFollowingPage).then(function (response) {
                        $scope.nextFollowingPage++;
                        $scope.addMore(response.data)
                    });
                }

            }
        };
        $scope.loadRecipeInPublicBooks = function (response) {
            for (i = 0; i < response.length; i++) {
                var recipe = new Recipe(response[i]);
                recipe.itemType = $scope.RECIPE;
                recipe.checkLoved($scope.userLovesList);
                $scope.exploreItems.push(recipe);
            }
        };

        // INITIALIZE FIRST RECIPES
        $scope.addMore(EXPLORE_PAGE);
        $scope.loadRecipeInPublicBooks(RECIPE_IN_PUBLIC_BOOKS);
    }]);

    // SERVICE TO ACCESS TO THE RECOMENDED CONTENT
    app.factory('RecomendedService', ['$http', function ($http) {
        return {
            recomendedRecipesUrl: RECOMMENDED_URL,
            getRecipes: function (page) {
                return $http.get(this.recomendedRecipesUrl + "?web=1&page=" + page);
            }
        }
    }]);

    // SERVICE TO ACCESS TO THE FOLLOWING CONTENT
    app.factory('FollowingService', ['$http', function ($http) {
        return {
            followingRecipesUrl: FOLLOWING_URL,
            getRecipes: function (page) {
                return $http.get(this.followingRecipesUrl + "?limit=30&page=" + page);
            }
        }
    }]);

}).call(this);

// REESTABLISHING THE STATUS AFTER BACK BUTTON
window.addEventListener("popstate", function (e) {
    scope = angular.element(document.getElementById('explore')).scope();
    scope.exploreItems = e.state.exploreItems;
    scope.nextRecomendedPage = e.state.nextRecomendedPage;
    scope.$apply();
});
