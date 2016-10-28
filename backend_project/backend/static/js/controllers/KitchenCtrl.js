var slug = function (str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();

    // remove accents, swap ñ for n, etc
    var from = "ãàáäâẽèéëêìíïîõòóöôùúüûñç·/_,:;";
    var to = "aaaaaeeeeeiiiiooooouuuunc------";
    for (var i = 0, l = from.length; i < l; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    return str;
};

app.controller('KitchenController', [
    '$scope',
    '$timeout',
    'Recipe',
    'Step',
    'Book',
    'Chef',
    '$location',
    '$window',
    'IngredientOnKitchenController',
    'BookSlideOnKitchenController',
    'AllergenOnKitchenController',
    'ToasterService',
    'RecipeOnKitchenController',
    KitchenController]);

if (window.define) define(function () {
    return KitchenController;
});

function KitchenController($scope,
                           $timeout,
                           Recipe,
                           Step,
                           Book,
                           Chef,
                           $location,
                           $window,
                           IngredientOnKitchenCtrl,
                           BookSlideCtrl,
                           AllergenOnKitchenController,
                           ToasterService,
                           RecipeOnKitchenController) {
    $scope.currentSlide = 1;
    $scope.recipe = null;
    $scope.selectedStep = null;
    $scope.tags = '';
    $scope.newBookName = '';
    $scope.loading = true;
    $scope.publishErrors = [];
    $scope.privateRecipe = false;
    $scope.addingBook = false;
    $scope.waitingToPublish = false;
    $scope.showUpgradeBanner = false;
    $scope.chef = null;
    this.$scope = $scope;
    $scope.ingredientCtrl = IngredientOnKitchenCtrl.newInstance();
    $scope.bookSlideCtrl = BookSlideCtrl.newInstance();
    $scope.allergenCtrl = AllergenOnKitchenController.newInstance($scope);
    $scope.recipeCtrl = RecipeOnKitchenController.newInstance($scope);

    try {
        $scope.deleteRecipeUrl = RECIPE_DELETE_URL;
    } catch (err) {
    }
    try {
        $scope.libraryUrl = LIBRARY_URL;
    } catch (err) {
    }
    try {
        $scope.pricingUrl = PRICE_URL;
    } catch (err) {
    }
    try {
        $scope.makePrivateUrl = MAKE_PRIVATE_RECIPE_URL;
    } catch (err) {
    }
    try {
        $scope.publishUrl = PUBLISH_RECIPE_URL;
    } catch (err) {
    }

    $scope.$on('updateIngredient', function (event, result) {
        $scope.ingredientList = result
    });

    $scope.setUpUpgradeBanner = function (idOfCurrentChef, membershipOfCurrentChef) {
        if (membershipOfCurrentChef == 'default') {
            if ($window.localStorage.getItem(idOfCurrentChef + "upgrade_banner_close")) {
                $('.kitchen-banner').css('display', 'none');
                $('.steps-content').css('top', 55);
                $scope.showUpgradeBanner = false;
            } else {
                $('.kitchen-banner').css('display', 'table');
                $('.steps-content').css('top', 115);
                $scope.showUpgradeBanner = true;
            }
        }
    };

    $scope.carouselSlide = function (carousel, direction) {
        $(carousel).carousel(direction);
    };

    $scope.init = function () {
        $scope.setUpUpgradeBanner(CHEF_ID, CHEF_MEMBERSHIP);

        $scope.recipe = new Recipe({'id': RECIPE_ID});
        $scope.recipe.loadRecipe().then(function (recipesData) {

            $scope.chef = new Chef({
                id: $scope.recipe.chef_id
            });

            $scope.ingredientCtrl.setRecipeOnModel($scope.recipe);
            $scope.ingredientCtrl.setChefOnModel($scope.chef);

            if ($scope.recipe.name == 'Unnamed Recipe') {
                $scope.recipe.name = '';
            }

            $scope.ingredientCtrl.initIngredient($scope.recipe.ingredients);


            var tags = $scope.recipe.tags;
            for (var i = 0; i < tags.length; i++) {
                $scope.tags += tags[i].name + ' ';
            }

            if ($scope.recipe.steps.length > 0) {
                // Selected the editting step at step 2
                $scope.selectedStep = $scope.recipe.steps[0];
                $scope.currentSlide = 2;
                // Selecting the existing cover if there is

                $("#cover_carousel").carousel({
                    pause: true,
                    interval: false
                });

                $('#cover_carousel').on('slid.bs.carousel', function () {
                    var active_item = $('#cover_carousel .active');
                    var scope = angular.element(active_item).scope();
                    scope.selectStepAsCoverById(parseInt(active_item.attr('data-id')));
                });

                if ($scope.recipe.getCover() != null) {

                    for (var i = 0; i < $scope.recipe.steps.length; i++) {
                        if ($scope.recipe.steps[i].cover == true) {
                            var cover_num = i;
                            $timeout(function () {
                                $("#cover_carousel").carousel(i);
                                $($("#cover_carousel .item")[cover_num]).addClass('active');
                            }, 500);
                        }
                    }
                    // Selecting the first image as cover otherwise
                } else {
                    $scope.recipe.selectCover($scope.recipe.steps[0]);
                    $timeout(function () {
                        $($("#cover_carousel .item")[0]).addClass('active');
                    }, 500);
                }

            } else {
                $scope.selectedStep = null;
                $scope.currentSlide = 1;
            }
            $scope.loading = false;

            $scope.allergenCtrl.onLoad($scope.recipe.allergens.split(", "));

        });

        $scope.bookSlideCtrl.createBookSlide(BOOKS);

        $scope.fn = {};

        $scope.subcribeAddingBook();

    };

    $scope.subcribeAddingBook = function () {
        $scope.$on('addingBookToSlide', function (event, data) {
            $scope.addNewBookToSlide(data.book);
        });
    };

    $scope.addNewBookToSlide = function (book) {
        $scope.bookSlideCtrl.addNewBook(book);
    };

    $scope.init();

    $scope.selectSlide = function (slide) {
        if (slide > 1 && $scope.recipe.steps.length > 0) {
            $scope.currentSlide = slide;
        } else {
            $scope.currentSlide = 1;
        }
    };

    $scope.selectStep = function (step) {
        if ($scope.selectedStep != null && $scope.selectedStep.changed == true) {
            $scope.selectedStep.changed = false;
            $scope.changeStepInstructions($scope.selectedStep);
        }
        $scope.selectedStep = null;
        $scope.selectedStep = step;
    };

    $scope.changeStepOrder = function (step) {
        step.updateOrder();
    };

    $scope.changeStepInstructions = function (step) {
        step.updateInstructions();
        step.changed = false;
        console.log('save');
    };

    $scope.deleteStep = function () {
        var step = $scope.selectedStep;
        var isCover = step.cover;
        $scope.recipe.deleteStep(step);
        if ($scope.recipe.steps.length > 0) {
            $scope.selectedStep = null;
            $scope.selectedStep = $scope.recipe.steps[0];
            // If we delete the cover, we select the new one
            if (isCover) {
                for (var i = 0; i < $scope.recipe.steps.length; i++) {
                    if ($scope.recipe.steps[i].cover == true) {
                        var cover_num = i;
                        $timeout(function () {
                            $($("#cover_carousel .item")[cover_num]).addClass('active');
                        }, 500);
                    }
                }
            }
        } else {
            $scope.selectedStep = null;
            $scope.currentSlide = 1;
        }
    };

    $scope.selectStepAsCover = function (step) {
        $scope.recipe.selectCover(step);
    };

    $scope.selectStepAsCoverById = function (stepId) {
        for (var i = 0; i < $scope.recipe.steps.length; i++) {
            if ($scope.recipe.steps[i].id == stepId) {
                $scope.recipe.selectCover($scope.recipe.steps[i]);
            }
        }
    };

    $scope.selectBook = function (book) {
        if ($scope.bookSlideCtrl.isBook(book)) {
            $scope.recipe.selectBook(book.id);
        } else {
            $scope.openBookModal();
        }
    };

    $scope.isBookSelected = function (book) {
        if ($scope.recipe.stepsLoaded) {
            return $scope.recipe.books_ids.indexOf(book.id) != -1;
        }
    };

    $scope.changeTitle = function () {
        $scope.recipe.editTitle();
    };

    $scope.changeServes = function () {
        $scope.recipe.editServes();
    };

    $scope.changePrepTime = function () {
        $scope.recipe.editPrepTime();
    };

    $scope.changeTags = function () {
        var temp = $scope.tags;
        temp = temp.replace(/\./g, '$');
        temp = temp.replace(/,/g, '$');
        temp = temp.replace(/#/g, '$');
        temp = temp.replace(/\s/g, '$');
        var temp_v = temp.split('$');
        var len = temp_v.length;
        while (len--) {
            if (temp_v[len] == '') {
                temp_v.splice(len, 1);
            }
        }
        for (var i = 0; i < temp_v.length; i++) {
            temp_v[i] = '#' + temp_v[i];
        }

        $scope.recipe.tags = temp_v;
        $scope.recipe.editTags();
    };

    $scope.addPhotos = function (photos) {
        var temporalSteps = [];
        for (var i = 0; i < photos.length; i++) {
            if ($scope.recipe.steps.length < 100) {
                var photo = photos[i];
                var step = new Step({recipe_id: $scope.recipe.id});
                if ($scope.selectedStep == null) {
                    $scope.selectedStep = step;
                }

                temporalSteps.push(step);

                step.order = $scope.recipe.steps.length + 1;
                step.uploadPhoto(photo, $scope, function (step, results) {

                    if ($scope.recipe.getCover() == null) {
                        $scope.recipe.selectCover(step);

                        $("#cover_carousel").carousel({
                            pause: true,
                            interval: false
                        });

                        $('#cover_carousel').on('slid.bs.carousel', function () {
                            var active_item = $('#cover_carousel .active');
                            var scope = angular.element(active_item).scope();
                            scope.selectStepAsCoverById(parseInt(active_item.attr('data-id')));
                        });

                        $timeout(function () {

                            var carousel_items = $("#cover_carousel .item");
                            for (var i = 0; i < carousel_items.length; i++) {
                                var item = $(carousel_items[i]);
                                if (parseInt(item.attr('data-id')) == step.id) {
                                    item.addClass('active');
                                } else {
                                    item.removeClass('active');
                                }
                            }

                        }, 500);
                    }

                    setTimeout(function () {
                        $scope.$apply(function () {
                        });
                    }, 0);
                });

                $scope.recipe.addStep(step);
                setTimeout(function () {
                    $scope.$apply(function () {
                    });
                }, 0);
            }
        }
        $scope.currentSlide = 2;
        $("#uploader_input").replaceWith($("#uploader_input").val('').clone(true));
    };

    $scope.openBookModal = function () {
        $scope.$broadcast('broadcast_add_book', {});
        $('#book_modal').modal('show');
    };

    $scope.checkSteps = function () {
        if ($scope.recipe.steps != undefined) {
            return $scope.recipe.steps.length > 0;
        } else {
            return false;
        }
    };

    $scope.checkPrepTime = function () {
        return $scope.recipe.prep_time != '' && $scope.recipe.prep_time != '0';
    };

    $scope.checkServes = function () {
        return $scope.recipe.serves != '' && $scope.recipe.serves != '0';
    };

    $scope.checkIngredients = function () {
        return $scope.ingredientList && $scope.ingredientList.length > 0;
    };

    $scope.checkTags = function () {
        return $scope.recipe.tags && $scope.recipe.tags.length > 0;
    };

    $scope.checkTitle = function () {
        return $scope.recipe.name != '' && $scope.recipe.steps.length > 0;
    };

    $scope.checkPublish = function () {
        if ($scope.recipe.books_ids != undefined) {
            return $scope.recipe.books_ids.length > 0;
        } else {
            return false;
        }
    };

    $scope.publish = function () {
        $scope.publishErrors = [];
        if (!$scope.checkSteps()) {
            $scope.publishErrors.push('You must upload at least 3 steps.');
        }
        if (!$scope.checkPrepTime()) {
            $scope.publishErrors.push('Your recipe is missing the preparation time.');
        }
        if (!$scope.checkServes()) {
            $scope.publishErrors.push('How many people are you cooking for? Set the serves number.');
        }
        if (!$scope.checkIngredients()) {
            $scope.publishErrors.push('What is your secret for this delicious dish? Complete the ingredients.');
        }
        if (!$scope.checkTags()) {
            $scope.publishErrors.push('Your recipe is missing the tags.');
        }
        if (!$scope.checkTitle()) {
            $scope.publishErrors.push('You must write a title.');
        }
        if (!$scope.checkPublish()) {
            $scope.publishErrors.push('You must select at least one book.');
        }
        if ($scope.publishErrors.length == 0) {

            if ($scope.addingBook == true) {
                $scope.waitingToPublish = true;

            } else {
                // Disabling the popup to exit
                window.onbeforeunload = function (e) {
                };

                if ($scope.recipe.private) {
                    document.location.href = ($scope.makePrivateUrl.replace('RECIPE_ID', this.recipe.id));
                    /*$scope.recipe.makePrivate().then(function(){
                     $scope.currentSlide = 6;
                     });*/
                } else {
                    document.location.href = ($scope.publishUrl.replace('RECIPE_ID', this.recipe.id));
                    /*$scope.recipe.publish().then(function(){
                     $scope.currentSlide = 6;
                     });*/
                }
            }

        } else {
            $('#publish_error_modal').modal("show");
        }
    };

    $scope.savePrivate = function () {
        $scope.recipe.private = true;
    };

    $scope.goBack = function () {
        if ($scope.recipe.steps == undefined || $scope.recipe.steps.length == 0) {
            // Disabling the popup to exit
            window.onbeforeunload = function (e) {
            };
            //delete recipe, redirects to library
            $window.location.href = (this.deleteRecipeUrl.replace('RECIPE_ID', this.recipe.id));
        }
        $window.location.href = (this.libraryUrl);
    };

    $scope.closeUpgradeBanner = function () {
        $window.localStorage.setItem(CHEF_ID + "upgrade_banner_close", true);
        $scope.setUpUpgradeBanner(CHEF_ID, CHEF_MEMBERSHIP);
    };

    $scope.redirectToPayement = function () {
        return $window.location.href = (this.pricingUrl);
    };

    $scope.saveDraft = function (_currentSilde) {
        // save ingredient
        $scope.ingredientCtrl.saveIngredients();
        // redirect to profile
        $window.location.href = (this.libraryUrl);
    };

    $scope.focusIngredient = function () {
        if ($scope.ingredientCtrl.showRecipesChain) {
            $scope.ingredientCtrl.showRecipesChain = false;
            return;
        }
        var ingredient_height = 240;
        var _offset = $scope.ingredientCtrl.ingredientInputTop;
        if (_offset - $scope.ingredientCtrl.ingredientContentScrollTop >= ingredient_height) {
            $('#ingredient_content').scrollTop(_offset + 100);
            _offset = 330;
        }

        $('.ingredient_suggestion_input').css('top', _offset);
        $('.ingredient_suggestion_result').css('top', _offset + 45);
        $scope.ingredientCtrl.showIngredientsSuggestion = true;

        setTimeout(function () {
            $scope.$apply(function () {
                $('#ingredient_suggestion_input').focus();
            });
        }, 0);
    };


    $scope.confirmIngredient = function () {
        $scope.ingredientCtrl.confirmIngredient(function () {
            $scope.selectIngredientSuggestionCallback();
        });
    };

    $scope.selectIngredientSuggestion = function (aIngredientName) {
        $scope.ingredientCtrl.selectIngredientSuggestion(aIngredientName, function () {
            $scope.selectIngredientSuggestionCallback();
        });
    };

    $scope.selectIngredientSuggestionCallback = function () {
        setTimeout(function () {
            $scope.$apply(function () {
                $scope.focusIngredient();

            });
        }, 0);
    };

    $scope.selectIngredient = function (aIngredient) {

    };

    $scope.showRecipesByIngredient = function (aIngredient, recipeIndex) {
        var showIndex = $scope.ingredientCtrl.showRecipesByIngredient(aIngredient);

        setTimeout(function () {
            $scope.$apply(function () {
                var currentScrollTopOffset = $('#ingredient_content').scrollTop();
                var recipeListScrollAtShowIndex = recipeIndex * 40;
                if (recipeListScrollAtShowIndex - currentScrollTopOffset + 250 > $('#ingredient_content').height()) {
                    var targetScrollTopOffset = recipeListScrollAtShowIndex - currentScrollTopOffset + 250;
                    $('#ingredient_content').scrollTop(targetScrollTopOffset);
                }

                $('#' + $scope.ingredientCtrl.currentRecipesByName.id).focus();
                $('#' + $scope.ingredientCtrl.currentRecipesByName.id).blur(function () {
                    if (!$scope.ingredientCtrl.showRecipesChain) {
                        $scope.ingredientCtrl.currentRecipesByName.show = false;
                        $scope.ingredientCtrl.hideRecipesByNameAtIndex(showIndex);
                        setTimeout(function () {
                            $scope.$apply(function () {
                            });
                        }, 0);
                    }
                });
                $('.dropdown-menu').mouseover(function () {
                    $scope.ingredientCtrl.showRecipesChain = true;
                });

                $('.dropdown-menu').mouseleave(function () {
                    $scope.ingredientCtrl.showRecipesChain = false;
                });

                $('#' + aIngredient.id).val(aIngredient.name);
            });
        }, 0);
    }

    $scope.loadmoreRecipes = function (aIngredient) {
        $scope.ingredientCtrl.loadmoreRecipes(aIngredient, function () {
            setTimeout(function () {
                $scope.$apply(function () {
                    $('#' + $scope.ingredientCtrl.currentRecipesByName.id).focus();
                });
            }, 0);
        });
    }

    $scope.toogleLinkToRecipe = function (recipeId, ingredient) {
        $scope.ingredientCtrl.toogleLinkToRecipe(recipeId, ingredient, function () {
            setTimeout(function () {
                $scope.$apply(function () {
                    $('#' + $scope.ingredientCtrl.currentRecipesByName.id).focus();
                });
            }, 0);
        });
    };

    $scope.redirectToDetail = function (recipe) {
        $window.location.href = '/recipe/' + slug(recipe.name) + '-' + recipe.linkRecipeId;
    };

    $scope.openDeleteImagePopup = function () {
        $('#delete_step_modal').modal('show');
    };
}

function facebook_share_dialog(evt) {
    evt.preventDefault();
    function callback(response) {
        //document.getElementById('msg').innerHTML = "Post ID: " + response['post_id'];
    }

    FB.ui(facebook_share_obj, callback);
}

function pinterest_share_dialog(evt) {
    evt.preventDefault();
    window.open(pinterest_share_obj, "_blank");
}

function set_window_height() {
    /*var original_height = $('.steps-content').outerHeight(true) + $('.steps-control').outerHeight(true);
     if( original_height < $(window).height()){
     $('.steps-content').height($(window).height() - $('.steps-control').height() - 6);
     }else{
     $('.steps-content').height('auto');
     }*/
}

$(document).ready(function () {

    $('body').css('background-color', '#181818');

    $('.steps-list').sortable({
        items: '>div:not(.add-step)',
        stop: function (event, ui) {
            var steps_list = $($(".steps-list")[0]);
            var steps = steps_list.find('.step:not(.add-step)');
            for (var i = 0; i < steps.length; i++) {
                var step = angular.element(steps[i]).scope().step;
                step.order = i + 1;
            }
            var scope = angular.element(ui.item[0]).scope();
            var step = ui.item.scope().step;
            scope.changeStepOrder(step);
            scope.$apply();
        }
    }).disableSelection();

    $('#uploader_button').mouseover(function () {
        $('.steps-content').addClass('drag');
    }).mouseleave(function () {
        $('.steps-content').removeClass('drag');
    });

    $('.steps-content').on('dragover', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass('drag');
    });

    $('.steps-content').on('dragenter', function (e) {
        e.preventDefault();
        e.stopPropagation();
        // $(this).addClass('drag');

    });

    $('.steps-content').on('dragstart', function (e) {
        e.preventDefault();
        e.stopPropagation();
        //$(this).addClass('drag');

    });

    $('.steps-content').on('dragleave', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('drag');
    });

    $('.steps-content').on('dragend', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('drag');
    });

    $('.steps-content').on('mouseleave', function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass('drag');
    });

    $('.steps-content').on('drop', function (e) {
        $(this).removeClass('drag');
        if (e.originalEvent.dataTransfer) {
            if (e.originalEvent.dataTransfer.files.length) {
                e.preventDefault();
                e.stopPropagation();
                var scope = angular.element(this).scope();
                scope.addPhotos(e.originalEvent.dataTransfer.files);
                scope.$apply();
            }
        }
    });

    $('#ingredient_content').scroll(function () {
        var scrollTopOffset = $('#ingredient_content').scrollTop();
        var scope = angular.element(this).scope();
        scope.ingredientCtrl.ingredientContentScrollTop = scrollTopOffset;
        scope.$apply();
    });


    $('#ingredient_suggestion_input').blur(function () {
        var scope = angular.element(this).scope();
        scope.ingredientCtrl.showIngredientsSuggestion = false;
        if (!scope.ingredientCtrl.hoverIngredientSuggestion)
            scope.ingredientCtrl.showIngredientSuggestionResult = false;
        scope.$apply();
    });

    $('#ingredient_suggestion_result').mouseover(function () {
        var scope = angular.element(this).scope();
        scope.ingredientCtrl.hoverIngredientSuggestion = true;
    });

    $('#ingredient_suggestion_result').mouseleave(function () {
        var scope = angular.element(this).scope();
        scope.ingredientCtrl.hoverIngredientSuggestion = false;
    });

    $('#recipes_dropdown').blur(function () {
        var scope = angular.element(this).scope();
        scope.ingredientCtrl.currentRecipesByName.show = false;
    });

    set_window_height();

    window.onresize = set_window_height;

    $('#facebook_share_button').click(facebook_share_dialog);
    $('#pinterest_share_button').click(pinterest_share_dialog);

    // GOODBYE POPUP
    window.onbeforeunload = function (e) {
        if (!e) e = window.event;
        //e.cancelBubble is supported by IE - this will kill the bubbling process.
        e.cancelBubble = true;
        //This is displayed on the dialog
        e.returnValue = 'Your recipe is saved in DRAFTS';
        //e.stopPropagation works in Firefox.
        if (e.stopPropagation) {
            e.stopPropagation();
            e.preventDefault();
        }
    };

});

