app.controller('BooksController', [
    '$scope', 'Book', 'Recipe', 'Chef', '$timeout', 'BookPresenter', 'BookModel',
    function ($scope, Book, Recipe, Chef, $timeout, Presenter, Model) {

        $scope.loadingRecipes = false;
        $scope.books = [];
        $scope.chefId = CHEF_ID;
        $scope.chefRecipes = [];
        $scope.chefRecipesCount = RECIPES_COUNT;
        $scope.currentChefRecipesPage = 2;
        $scope.bookRecipesCount = 0;
        $scope.bookRecipesTotal = 0;
        $scope.drafts = [];
        $scope.userLovesList = USER_LOVES_LIST;
        $scope.currentBookId = [];
        $scope.currentRecipes = [];
        $scope.loadingMore = false;
        $scope.currentBook;

        $scope.newBookName = '';
        $scope.bookToEdit = null;
        $scope.bookToEditOldName = '';
        $scope.bookToDelete = null;
        $scope.draftToDelete = null;
        $scope.collaborators = {};

        this.presenter = $scope.presenter = Presenter.newInstance();
        this.model = $scope.model = Model.newInstance();
        $scope.events = this.presenter.show($scope, this.model);

        for (var i = 0; i < BOOKS.length; i++) {
            var book = new Book(BOOKS[i]);
            $scope.books.push(book);
        }

        for (var i = 0; i < DRAFTS.length; i++) {
            var draft = new Recipe(DRAFTS[i]);
            draft.checkLoved($scope.userLovesList);
            $scope.drafts.push(draft);
        }

        for (var i = 0; i < RECIPES.length; i++) {
            var recipe = new Recipe(RECIPES[i]);
            recipe.checkLoved($scope.userLovesList);
            $scope.chefRecipes.push(recipe);
        }

        $scope.commentsLine = function (recipe, number) {
            return recipe.last_comments.length == number;
        };

        $scope.setBookToEdit = function (book) {
            $scope.bookToEdit = book;
            $scope.bookToEditOldName = book.name;
            $scope.$broadcast('broadcast_edit_book', {editBook: book});
        };

        $scope.$on('emit_cancel_edit_book', function (event, args) {
            console.log(args.book);
            // $scope.bookToEdit = args.book;
        });

        $scope.$on('emit_update_book', function (event, args) {
            $scope.editBook(args.book);
        });

        $scope.setBookToDelete = function (book) {
            $scope.bookToDelete = book;
        };

        $scope.showChefRecipes = function () {
            /*if ($scope.chefRecipes.length == 0) {
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
             } else {*/
            $scope.currentRecipes = $scope.chefRecipes;
            $scope.currentBookId = 'chefRecipes';
            $scope.currentBook = {};
            window.location.hash = '#recipes';
        };

        $scope.loadMoreChefRecipes = function () {
            var chef = new Chef({
                id: $scope.chefId
            });
            $scope.loadingMore = true;
            chef.loadRecipes($scope.currentChefRecipesPage).then(function (recipesArray) {
                for (var i = 0; i < recipesArray.data.results.length; i++) {
                    var recipe = new Recipe(recipesArray.data.results[i]);
                    recipe.checkLoved($scope.userLovesList);
                    $scope.chefRecipes.push(recipe);
                }
                $scope.currentChefRecipesPage++;
                $scope.loadingMore = false;
            })
        };

        $scope.showDrafts = function () {
            $scope.loadingRecipes = true;
            $scope.currentRecipes = $scope.drafts;
            $scope.currentBookId = 'drafts';
            $scope.loadingRecipes = false;
            window.location.hash = '#drafts';
        };

        $scope.showBookRecipesById = function (bookId) {
            if (bookId == 'allrecipes') {
                $scope.showChefRecipes();
            } else {
                for (var i = 0; i < $scope.books.length; i++) {
                    if ($scope.books[i].id == parseInt(bookId)) {
                        $scope.showBookRecipes($scope.books[i]);
                        break;
                    }
                }
            }
        };

        $scope.showBookRecipes = function (book) {
            $scope.loadingRecipes = true;
            $scope.currentBookId = book.id;
            $scope.currentBook = book;
            if (book.recipes == undefined) {
                book.setPage(1);
                book.loadRecipes().then(function (recipesArray) {
                    book.setTotalRecipes(recipesArray.data.count);
                    $scope.bookRecipesTotal = book.TotalRecipes;
                    $scope.currentRecipes = [];
                    for (var i = 0; i < book.recipes.length; i++) {
                        book.recipes[i].checkLoved($scope.userLovesList);
                    }
                    $scope.bookRecipesCount = book.recipes.length;
                    $scope.currentRecipes = book.recipes;
                    $scope.loadingRecipes = false;
                });
            } else {
                $scope.currentRecipes = book.recipes;
                $scope.bookRecipesTotal = book.TotalRecipes;
                $scope.bookRecipesCount = book.recipes.length;
                $scope.loadingRecipes = false;
            }
            window.location.hash = '#' + slug(book.name) + '-' + book.id;
        };

        $scope.loadMoreBookRecipes = function () {
            $scope.loadingMore = true;
            $scope.currentBook.loadRecipes().then(function (recipesArray) {
                $scope.currentRecipes = [];
                for (var i = 0; i < $scope.currentBook.recipes.length; i++) {
                    $scope.currentBook.recipes[i].checkLoved($scope.userLovesList);
                }
                $scope.currentRecipes = $scope.currentBook.recipes;
                $scope.bookRecipesCount = $scope.currentBook.recipes.length;
                $scope.loadingMore = false;
            });
        };

        $scope.addNewBook = function (newBookName) {
            var book = new Book();
            book.create(newBookName).then(function (response) {
                $scope.books.push(book);
                $scope.newBookName = '';
            });
        };

        $scope.editBook = function (book) {
            book.edit().then(function (response) {
                $scope.bookToEdit = null;
            });
        };

        $scope.deleteBook = function (book) {
            book.delete().then(function (response) {
                var index = $scope.books.indexOf(book);
                $scope.books.splice(index, 1);
                $scope.bookToDelete = null;
            });
        };

        $scope.init = function () {
            var hash = window.location.hash;
            if (hash == '#drafts') {
                $scope.showDrafts();
            }
            else if (hash == '#recipes') {
                window.location.hash = '#recipes';
                $scope.currentBookId = 'chefRecipes';
                $scope.currentRecipes = $scope.chefRecipes;
            }
            else if (hash != '') {
                var splitted = hash.split('-');
                for (var i = 0; i < $scope.books.length; i++) {
                    if ($scope.books[i].id == splitted[1]) {
                        $scope.showBookRecipes($scope.books[i]);
                        break;
                    }
                }
            }
            else {
                window.location.hash = '#recipes';
                $scope.currentBookId = 'chefRecipes';
                $scope.currentRecipes = $scope.chefRecipes;
            }

            $scope.subcribeAddingBook();
        };

        $scope.subcribeAddingBook = function () {
            $scope.$on('addingBookToSlide', function (event, data) {
                $scope.addNewBookToList(data.book);
            });
        };

        $scope.addNewBookToList = function (book) {
            $scope.books.push(new Book(book));
        };

        $scope.setDraftToDelete = function (draft) {
            $scope.draftToDelete = draft;
        };

        $scope.deleteDraft = function (draft) {
            draft.deleteRecipe().then(function () {
                var index = $scope.drafts.indexOf(draft);
                $scope.drafts.splice(index, 1);
            });
        };

        $scope.init();

        $scope.redirectTo = function (url) {
            window.location.href = url;
        };

        $scope.showError = function (error) {
            return new Error(error);
        };

        $scope.initAddBookModal = function () {
            $scope.collaboratorField = '';
            $scope.isShowCollaboratorDropdown = false;
            $scope.$broadcast('broadcast_add_book', {});
        };

        var _timeout;
        $scope.getCollaborator = function (name) {
            // Because using old angular version 1.2.0, not support debounce, we using timeout.
            if (_timeout) {
                $timeout.cancel(_timeout);
            }
            _timeout = $timeout(function () {
                if (name === '') {
                    $scope.isShowCollaboratorDropdown = false;
                } else {
                    $scope.presenter.handleOnChangeGetCollaborator($scope, $scope.model, name);
                }
                _timeout = null;
            }, 800);
        };

        $scope.initCollaboratorDropdown = function (response) {
            $scope.collaborators.chefs = response.chefs;
            $scope.collaborators.readmore = response.readmore;
            $scope.isShowCollaboratorDropdown = true;
            $scope.collaboratorDropdownPaging = $scope.collaboratorDropdownPaging || 1;
        };

        $scope.loadmoreCollaborator = function (name, page) {
            $scope.collaboratorDropdownPaging = page + 1;
            $scope.presenter.handleOnChangeGetCollaborator($scope, $scope.model, name, $scope.collaboratorDropdownPaging);
        };
    }]);