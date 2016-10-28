app.factory('Book', ['$http', 'Recipe', function ($http, Recipe) {

    function Book(bookData) {
        if (bookData) {
            this.setData(bookData);
        }
    }

    Book.prototype = {
        addBookUrl: BOOK_ADD_URL,
        editBookUrl: BOOK_EDIT_URL,
        addRecipeUrl: BOOK_ADD_RECIPE_URL,
        deleteBookUrl: BOOK_DELETE_URL,
        loadRecipesUrl: BOOK_LIST_RECIPES_URL,
        setData: function (bookData) {
            angular.extend(this, bookData);
        },
        setRecipes: function (recipesArray) {
            for (var i = 0; i < recipesArray.length; i++) {
                this.recipes.push(new Recipe(recipesArray[i]));
            }
        },
        create: function (bookName) {
            this.name = bookName;
            var scope = this;
            return $http.post(this.addBookUrl, $.param({name: this.name})).success(function (bookData) {
                scope.setData(bookData.book_data);
            });            //this.nb_recipes = this.recipes.length;

        },
        delete: function () {
            var scope = this;
            return $http.post(this.deleteBookUrl.replace('BOOK_ID', this.id)).success(function (result) {

            });
        },
        edit: function () {
            var scope = this;
            var private;
            if (this.private === false)
                private = 0;
            else if (this.private === true)
                private = 1;
            else
                private = this.private;
            
            return $http.post(this.editBookUrl.replace('BOOK_ID', this.id), $.param({
                name: this.name,
                private: private,
                collaborators: this.collaborators
            })).success(function (result) {

            });
        },
        addRecipe: function (recipe_id) {
            var scope = this;
            return $http.post(this.addRecipeUrl.replace('BOOK_ID', this.id).replace('RECIPE_ID', recipe_id)).success(function (result) {

            });
        },
        checkAdded: function (booksList) {
            for (var i = 0; i < booksList.length; i++) {
                if (parseInt(this.id) == parseInt(booksList[i])) {
                    this.added = true;
                    return true;
                }
            }
            this.added = false;
            return false;
        },
        loadRecipes: function () {
            var scope = this;
            return $http.get(this.loadRecipesUrl.replace('BOOK_ID', this.id) + '?page=' + scope.page).success(function (recipes) {
                scope.setRecipes(recipes.results);
                scope.page++;
            });
        },
        setTotalRecipes: function (length) {
            var scope = this;
            scope.TotalRecipes = length;
        },
        setPage: function (value) {
            var scope = this;
            scope.page = value;
            scope.recipes = [];
        },
        addBook: function (body) {
            var scope = this;
            return $http.post(this.addBookUrl, $.param(body)).success(function (bookData) {
                scope.setData(bookData.book);
            });
        }
    };
    return Book;
}]);