;(function(app, window) {
    app.factory('Chef', ['$http', function($http) {

        function Chef(chefData) {
            try {
                this.followUrl = CHEF_FOLLOW_URL;
            }catch(err) { }
            try {
                this.loadFollowingUrl = CHEF_LOAD_FOLLOWING_URL;
            }catch(err) { }
            try {
                this.loadFollowersUrl = CHEF_LOAD_FOLLOWERS_URL;
            }catch(err) { }
            try {
                this.uploadRestaurantImageUrl = CHEF_UPLOAD_RESTAURANT_IMAGE_URL;
            }catch(err) { }
            try {
                this.uploadAvatarImageUrl = CHEF_UPLOAD_AVATAR_IMAGE_URL;
            }catch(err) { }
            try {
                this.uploadCoverImageUrl = CHEF_UPLOAD_COVER_IMAGE_URL;
            }catch(err) { }
            try {
                this.loadRecipesUrl = CHEF_RECIPES_URL;
            }catch(err) { }
            try {
                this.loadRecipesByNameUrl = CHEF_RECIPES_BY_NAME_URL;
            }catch(err) { }

            if (chefData) {
                this.setData(chefData);
            }
        }

        Chef.prototype = {

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
                return $http.post(this.followUrl, $.param({chef_id: this.id,})).success(function(follower_data) {
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

        Chef.getChefByNameLimit = function(name, page) {
            page = page || 1;
            return $http.get(CHEF_GET_BY_NAME_AND_LIMIT + '?chef_name=' + name + '&page_limit=' + page);
        };

        return Chef;
    }]);
})(app, this);