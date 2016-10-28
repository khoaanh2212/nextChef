(function () {

    app.controller("RecipeController", ['$scope', 'Recipe', 'Chef', 'Book', '$http', function ($scope, Recipe, Chef, Book, $http) {
        $scope.chef;
        $scope.recipe;
        $scope.recipeId;
        $scope.chefId;
        $scope.userLovesList;
        $scope.userFollowingList;
        $scope.userBooksList;
        $scope.userRecipeInBooksList;
        $scope.showBooksDropdown = false;
        $scope.showShareDropdown = false;
        $scope.showBooksDropdownUnder = false;
        $scope.nb_likes;
        $scope.nb_added;

        $scope.init = function () {
            $scope.chef = new Chef({id: $scope.chefId});
            $scope.chef.checkFollowed($scope.userFollowingList);

            $scope.recipe = new Recipe({
                id: $scope.recipeId,
                nb_likes: $scope.nb_likes,
                nb_added: $scope.nb_added
            });
            $scope.recipe.checkLoved($scope.userLovesList);

            for (var i = 0; i < $scope.userBooksList.length; i++) {
                $scope.userBooksList[i] = new Book($scope.userBooksList[i]);
                $scope.userBooksList[i].checkAdded($scope.userRecipeInBooksList);
            }

            $('#buy_book_modal').modal('show');

        };

        $scope.$on('emit_GrossProfit_FoodCost', function (events, args) {
            $scope.gross_profit = args.gross_profit;
            $scope.food_cost = args.food_cost;
            $scope.changePricing();
        });

        $scope.$on('emit_VAT', function (events, args) {
            $scope.vat = args.vat;
            $scope.changePricing();
        });

        $scope.$on('emit_Servings', function (events, args) {
            $scope.servings = args.servings;
            $scope.oldServings = args.oldServings
            $scope.changePricing();
        });

        $scope.loveRecipe = function () {
            checkAuthenticated('love');
            if (USER_AUTHENTICATED) {
                $scope.recipe.love().then(function () {
                });
            }
        };

        $scope.changePricing = function () {
            if (USER_AUTHENTICATED) {
                var body = {
                    grossProfit: $scope.gross_profit || 0,
                    foodCost: $scope.food_cost || 0,
                    vat: $scope.vat || 0,
                    serves: $scope.servings || 0,
                    oldServes: $scope.oldServings || 0,
                };

                $http.post('/recipe/edit/pricing/' + RECIPE_ID + '/', body).then(function (response) {
                    if (response.data.success == true) {
                        $scope.oldServings = $scope.servings;
                    }
                    $scope.$broadcast('broadcast_finish_update_pricing', {success: response.data.success});
                });
            }
        };

        $scope.follow = function () {
            checkAuthenticated('follow');
            if (USER_AUTHENTICATED) {
                if ($scope.chef.followed) {
                    var chef_index = $scope.userFollowingList.indexOf($scope.chef.id);
                    $scope.userFollowingList.splice(1, chef_index);
                    $scope.chef.followed = false;
                    $scope.chef.follow().then(function (response) {
                        if (!response.data.success) {
                            $scope.userFollowingList.push($scope.chef.id);
                            $scope.chef.followed = true;
                        }
                    });
                } else {
                    $scope.userFollowingList.push($scope.chef.id);
                    $scope.chef.followed = true;
                    $scope.chef.follow().then(function (response) {
                        if (!response.data.success) {
                            var chef_index = $scope.userFollowingList.indexOf($scope.chef.id);
                            $scope.userFollowingList.splice(1, chef_index)
                            $scope.chef.followed = false;
                        }
                    });
                }
            }
        };

        $scope.showBooksList = function (book) {
            checkAuthenticated('add');
            if (USER_AUTHENTICATED) {
                $scope.showBooksDropdown = !$scope.showBooksDropdown;
                $scope.showShareDropdown = false;
                $scope.showBooksDropdownUnder = false;
            }
        };

        $scope.showBooksListUnder = function (book) {
            checkAuthenticated('add');
            if (USER_AUTHENTICATED) {
                $scope.showBooksDropdownUnder = !$scope.showBooksDropdownUnder;
                $scope.showBooksDropdown = false;
                $scope.showShareDropdown = false;
            }
        };

        $scope.showShareList = function (book) {
            $scope.showShareDropdown = !$scope.showShareDropdown;
            $scope.showBooksDropdown = false;
            $scope.showBooksDropdownUnder = false;
        };

        $scope.addRecipeToBook = function (book) {
            checkAuthenticated('add');
            if (USER_AUTHENTICATED) {
                if (book.added) {
                    $scope.nb_added--;
                }
                else {
                    $scope.nb_added++;
                }
                book.addRecipe($scope.recipeId).then(function (response) {
                    if (response.data.success) {
                        if (response.data.added) {
                            book.added = true;
                        } else {
                            book.added = false;
                        }
                    }
                    else {
                        if (book.added) {
                            $scope.nb_added++;
                        }
                        else {
                            $scope.nb_added--;
                        }
                    }
                });
            }
        };

        $scope.goToComments = function () {
            $('body').scrollTo('#comments_row', {duration: 'slow'});
        }

        $scope.createBook = function (bookName) {
            checkAuthenticated('add');
            if (USER_AUTHENTICATED) {
                var book = new Book();
                book.create(bookName).then(function (response) {
                    if (response.data.success) {
                        $scope.userBooksList.push(book);
                        var books_list;
                        if ($scope.showBooksDropdown) books_list = $('#dropdown_books_list');
                        else if ($scope.showBooksDropdownUnder) books_list = $('#dropdown_books_list_under');
                        else return;
                        books_list.animate({scrollTop: books_list[0].scrollHeight}, 500);
                        $scope.addRecipeToBook(book);

                    }
                });
            }
        };

        $scope.embedShare = function () {
            var popup = $('#embed_popup');
            if (popup.is(':active')) {
                popup.fadeOut(300);
            } else {
                popup.fadeIn(300);
            }
        };

        $scope.facebookShare = function () {
            FB.ui(facebook_share_obj, function (response) {
            });
        };

        $scope.pinterestShare = function () {
            window.open(pinterest_share_obj, "_blank");
        };

        $scope.showDeleteModal = function () {
            $('#delete_recipe_modal').modal('show');
        };

        $scope.followById = function (id, followed) {
            var chef = new Chef({'id': id});
            chef.follow().then(function (response) {
                if (!response.data.success) {
                    if (!followed) {
                        $('#chef-' + id).removeClass('following');
                        $('#chef-' + id).text('+');
                    }
                    else {
                        $('#chef-' + id).addClass('following');
                        $('#chef-' + id).text('-');
                    }
                }
            });
        };


    }]);

}).call(this);


$(document).ready(function () {
    scope = angular.element(document.getElementById('recipe')).scope();
    scope.init();
    scope.$apply();

    /* START RESPONSIVE STEP IMAGES */
    var imageHeight, wrapperHeight, overlap, container = $('.image');

    function centerImage() {
        imageHeight = container.find('img').height();
        wrapperHeight = container.height();
        overlap = (wrapperHeight - imageHeight) / 2;
        container.find('img').css('margin-top', overlap);
    }

    $(window).on("load resize", centerImage);

    var chefs = $('.follow-button');
    for (var i = 0; i < chefs.length; i++) {
        var CHEF_ID = chefs[i].attributes[1].value;
        for (var j = 0; j < USER_FOLLOWINGS_LIST.length; j++) {
            if (CHEF_ID == USER_FOLLOWINGS_LIST[j]) {
                $('#chef-' + CHEF_ID).addClass('following');
                $('#chef-' + CHEF_ID).text('-');
                break;
            }
        }
    }
    ;
    /* END RESPONSIVE STEP IMAGES */

    $('.follow-button').click(function (evt) {
        evt.preventDefault();
        checkAuthenticated('follow');
        if (USER_AUTHENTICATED) {
            var chefID = parseInt($(this).attr('data-chef-id'));
            if ($(this).hasClass('following')) {
                $(this).removeClass('following');
                $(this).text('+');
                scope.followById(chefID, true);
            }
            else {
                $(this).addClass('following');
                $(this).text('-');
                scope.followById(chefID, false);
            }
        }
    });

    $('#embed_popup').click(function () {
        $(this).fadeOut(300);
    });

    $('#embed_popup .content').click(function (evt) {
        evt.stopPropagation();
        evt.preventDefault();
    });

    $('#dropdown_ingredients').click(function (evt) {
        evt.preventDefault();
        var list = $('#ingredients_list');
        if (list.is(":visible")) {
            list.slideUp(300);
            $(this).removeClass('active');
        } else {
            list.slideDown(300);
            $(this).addClass('active');
        }
    });

    $('#fullscreen_close_button').click(function (evt) {
        evt.preventDefault();
        $('#fullscreen_view_modal').fadeOut(300);
    });

    $('.step').click(function () {
        var slide = parseInt($(this).attr('data-slide-number'));
        $('#fullscreen-steps-carousel').carousel(slide);
        $('#fullscreen_view_modal').fadeIn(300);
    });

    var grid_view = true;
    var layouts = $('#steps_list .step .layout');
    var buttons = $('#steps_list .step .top-change-view-area');
    var descriptions = $('#steps_list .description');

    $('#steps_list .top-change-view-area, #steps_list .bottom-change-view-area').click(function (evt) {
        evt.preventDefault();
        evt.stopPropagation();
        if (grid_view) {
            grid_view = false;
            //layouts.fadeOut(300, function(){});
            descriptions.slideDown(300, function () {
                layouts.fadeOut(100);
                buttons.fadeOut(50);
            });

        } else {
            grid_view = true;
            //descriptions.slideUp(500, function(){layouts.fadeIn(0);});
            descriptions.slideUp(300, function () {
                layouts.css('display', 'block');
                buttons.css('display', 'block');
            });


        }
    });

    var max_height = 0;
    var descriptions = $('#steps_list .description');
    for (var i = 0; i < descriptions.length; i++) {
        var current_height = $(descriptions[i]).height();
        if (max_height < current_height) max_height = current_height;
    }
    descriptions.height(max_height);

    $('#new_comment_button').click(function (evt) {
        evt.preventDefault();

        var new_comment = $('#new_comment');

        if (new_comment.val() != '') {

            var form_data = {
                "comment": new_comment.val()
            }

            var csrftoken = getCookie('csrftoken');

            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                type: 'POST',
                url: $(this).attr('data-comment-recipe-url'),
                dataType: "json",
                data: form_data,
                success: function (data) {
                    if (data.success == true) {
                        new_comment.val('');

                        var comment = "<div class='comment col-xs-12 col-sm-12 col-md-12 col-lg-12'>" +
                            "<div class='col-xs-12 col-sm-2 col-md-2 col-lg-2'>" +
                            "<div class='avatar' style='background-image:url(" + data.photo + ")'></div>" +
                            "</div>" +
                            "<div class='col-xs-12 col-sm-10 col-md-10 col-lg-10'>" +
                            "<p class='sender'>" + data.first_name + "</p>" +
                            "<p class='text'>" + data.comment + "</p>" +
                            "<p class='date'>" + data.date + "</p>" +
                            "</div>" +
                            "</div>";

                        comment = $(comment);

                        $('.new-comment').before(comment);
                    }
                    var commentCount = $('.nb-comments');
                    var number = parseInt(commentCount.text());
                    commentCount.text(number + 1);
                },
                error: function (data) {
                    console.log(data);
                }
            });
        }
    });

    //checkAuthenticated('recipe');

    $('[data-toggle="tooltip"]').tooltip();

    setTimeout(function () {
        $('.add-tooltip').fadeIn(300);
    }, 1000);
    $('.add-tooltip').mouseout(function () {
        $('.add-tooltip').fadeOut(300);
    });


});

