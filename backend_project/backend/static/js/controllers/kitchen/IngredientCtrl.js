/**
 * Created by apium on 01/04/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['$scope', '$timeout', 'IngredientPresenter', 'IngredientModel', 'ToasterService'];

    app.controller("IngredientController", deps.concat([function ($scope, $timeout, presenter, model, toaster) {
        IngredientController.$scope = $scope;
        IngredientController.$timeout = $timeout;
        IngredientController.presenter = presenter;
        IngredientController.model = model;
        IngredientController.toaster = toaster;
        return IngredientController.newInstance();
    }]));

    if (window.define) define(function () {
        return IngredientController;
    });

    function IngredientController($scope, $timeout, presenter, model, toaster) {
        this.$scope = $scope;
        this.$timeout = $timeout;
        this.presenter = presenter;
        this.model = model;
        this.$scope.toaster = toaster;
        this.$scope.events = this.presenter.show(this, this.model);
        this._initFn();
    }

    IngredientController.newInstance = function ($scope, $timeout, presenter, model, toaster) {
        return new IngredientController(
            $scope || IngredientController.$scope,
            $timeout || IngredientController.$timeout,
            presenter || IngredientController.presenter.newInstance(),
            model || IngredientController.model.newInstance(),
            toaster || IngredientController.toaster.newInstance()
        );
    };

    IngredientController.prototype._initFn = function () {
        this.$scope.fn = {
            onChangeGetDropdownList: this.onChangeGetDropdownList.bind(this),
            onConfirmDelete: this.confirmDelete.bind(this),
            redirect: this.redirect.bind(this),
            tooltip: this.tooltip.bind(this),
            checkEnable: this.checkEnable.bind(this),
            onHandleKeyDownOnInputIngredient: this.handleKeyDownOnInputIngredient.bind(this)
        };
    };

    IngredientController.prototype.init = function (list) {
        this.onClickOutSideDropdown();
        this.onUpdateRecipeDetails(list);
    };

    IngredientController.prototype.onUpdateRecipeDetails = function (list) {
        this.$scope.list = list.ingredientList;
        this.$scope.$emit('updateAllergens', list.allergens);
        this.$scope.$emit('updateIngredient', list.ingredientList)
    };

    IngredientController.prototype.showError = function (error) {
        console.log(error);
    };

    IngredientController.prototype.onChangeGetDropdownList = function () {
        var self = this;
        var $scope = self.$scope;

        if (self._timeout) self.$timeout.cancel(self._timeout);
        self._timeout = self.$timeout(function () {
            $scope.waitingServer = true;
            $scope.isSelectedItem = false;
            $scope.events.getIngredientList($scope.ingredientField);
            self._timeout = null;
        }, 800);
    };

    IngredientController.prototype.showDropdownList = function (dropdown) {
        this.$scope.isShowDropdownList = dropdown.isShow;
        this.$scope.ingredientList = dropdown.ingredients;
        this.$scope.recipeList = dropdown.recipes;
        this.$scope.isShowMoreIngredient = dropdown.ingredients.has_more;
        this.$scope.isShowMoreRecipe = dropdown.recipes.has_more;
        this.$scope.waitingServer = false;
        this.$scope.waitingAdding = false;
    };

    IngredientController.prototype.hideDropdownList = function () {
        this.$scope.isShowDropdownList = false;
    };

    IngredientController.prototype.executeSelectedIngredient = function (selected) {
        this.hideDropdownList();
        this.$scope.ingredientField = selected.ingredient || selected.name;
        this.$scope.isSelectedItem = true;
        $('.ingredient-field input').focus();
    };

    IngredientController.prototype.onClickOutSideDropdown = function () {
        var self = this;
        $(document).off('click').on('click', function (e) {
            $.each($('.ingredient-field'), function () {
                if (this !== e.target && !$(this).has(e.target).length && !$(this).is('.dropdown-list')) {
                    self.hideDropdownList();
                    if (!self.$scope.$$phase) self.$scope.$apply();
                }
            });
        });
    };

    IngredientController.prototype.addSuccess = function (response) {
        this.hideDropdownList();
        if (response.invalid) {
            this.toasterWithTemplate(response.msg, 'danger');
            return;
        }

        this.$scope.waitingAdding = false;
        this.$scope.amountField = '';
        this.$scope.ingredientField = '';
        this.$scope.list = response.ingredientList;
        if (response.message == '') {
            this.$scope.toaster.sendAlert({
                msg: 'Your allergens have been updated',
                type: 'success'
            });
        } else {
            this.$scope.toaster.sendAlert({
                msg: response.message,
                type: 'success'
            });
        }

        this.$scope.events.onUpdateRecipe();
        var list = this.$scope.list;
        setTimeout(function () {
            $('#listIngredient').animate({scrollTop: (list.length * 44)});
        }, 200);

    };

    IngredientController.prototype.toasterWithTemplate = function (msg, type) {
        this.$scope.toaster.sendAlert({
            msg: msg,
            type: type
        });
    };

    IngredientController.prototype.toasterError = function () {
        this.$scope.toaster.sendAlert({
            msg: "Cannot update allergens with Edamam. Please try again later!",
            type: 'danger'
        });
    };

    IngredientController.prototype.deleteSuccess = function (response) {
        this.$scope.list = response.ingredientList;
        this.$scope.toaster.sendAlert({
            msg: 'Your ingredient has been deleted',
            type: 'success'
        });
        this.$scope.$emit('updateAllergens', response.allergens);
        this.$scope.$emit('updateIngredient', response.ingredientList);
    };

    IngredientController.prototype.confirmDelete = function (ingredient) {
        this.$scope.deleteItem = ingredient;
        $('#delete-modal').modal('show');
    };

    IngredientController.prototype.redirect = function (link) {
        window.open(link, '_blank');
    };

    IngredientController.prototype.tooltip = function (event) {
        var element = $(event.target);
        element.tooltip();
    };

    IngredientController.prototype.checkEnable = function () {
        if (this.$scope.isSelectedItem) {
            this.$scope.waitingAdding = false;
        }
    };

    IngredientController.prototype.returnEmpty = function () {
        return {};
    };

    IngredientController.prototype.handleKeyDownOnInputIngredient = function ($event) {
        var $listIngredient = $('.lst-ingredient').find('li');
        var $listSubRecipe = $('.lst-sub-recipe').find('li');
        var $selectedIngredient = $listIngredient.filter('.selected');
        var $selectedSubRecipe = $listSubRecipe.filter('.selected');
        var $current;
        $listIngredient.removeClass('selected');
        $listSubRecipe.removeClass('selected');
        var dropDownData = {
            listIngredient: $listIngredient,
            listSubRecipe: $listSubRecipe,
            selectedIngredient: $selectedIngredient,
            selectedSubRecipe: $selectedSubRecipe,
        };

        if ($event.which === 40) {
            if (!this.$scope.isShowDropdownList)
                return false;
            $current = this.handleMoveDownOnDropDown(dropDownData);
        } else if ($event.which === 38) {
            if (!this.$scope.isShowDropdownList)
                return false;
            $current = this.handleMoveUpOnDropDown(dropDownData);
        } else if ($event.which === 13) {
            if (this.$scope.ingredientField && !this.$scope.waitingAdding
                && $selectedIngredient.html() == undefined && $selectedSubRecipe.html() == undefined) {
                this.$scope.waitingAdding = true;
                this.$scope.events.onAddingIngredient({
                    amount: this.$scope.amountField,
                    ingredient: this.$scope.ingredientField
                })
            }
            else
                this.handleChooseIngredientFromDropDownByEnter(dropDownData);
        }
        if ($current) {
            $current.addClass('selected');
        }
    };

    IngredientController.prototype.handleMoveDownOnDropDown = function (dropDownData) {
        var $current;
        if ((!dropDownData.selectedIngredient.length && !dropDownData.selectedSubRecipe.length)
            || dropDownData.selectedSubRecipe.is(':last-child'))
            $current = dropDownData.listIngredient.first();
        else if (dropDownData.selectedIngredient.is(':last-child'))
            $current = dropDownData.listSubRecipe.first();
        else {
            if (dropDownData.selectedIngredient.html())
                $current = dropDownData.selectedIngredient.next();
            else if (dropDownData.selectedSubRecipe.html()) {
                $current = dropDownData.selectedSubRecipe.next();
            }
        }
        if ($current)
            $current.closest('div.dropdown-list').scrollTop($current.index() * $current.outerHeight());
        return $current;
    };

    IngredientController.prototype.handleMoveUpOnDropDown = function (dropDownData) {
        var $current;
        if ((!dropDownData.selectedIngredient.length && !dropDownData.selectedSubRecipe.length)
            || dropDownData.selectedIngredient.is(':first-child'))
            $current = dropDownData.listSubRecipe.last();
        else if (dropDownData.selectedSubRecipe.is(':first-child'))
            $current = dropDownData.listIngredient.last();
        else {
            if (dropDownData.selectedIngredient.html())
                $current = dropDownData.selectedIngredient.prev();
            else if (dropDownData.selectedSubRecipe.html())
                $current = dropDownData.selectedSubRecipe.prev();
        }
        if ($current)
            $current.closest('div.dropdown-list').scrollTop($current.index() * $current.outerHeight());
        return $current;
    };

    IngredientController.prototype.handleChooseIngredientFromDropDownByEnter = function (dropDownData) {
        if (dropDownData.selectedIngredient.index() > -1) {
            var index = dropDownData.selectedIngredient.index();
            if (index < this.$scope.ingredientList.list.length)
                this.$scope.events.onSelectIngredient(this.$scope.ingredientList.list[index]);
            else
                this.$scope.events.onShowMoreIngredient();
        }
        if (dropDownData.selectedSubRecipe.index() > -1) {
            var index = dropDownData.selectedSubRecipe.index();
            if (index < this.$scope.recipeList.list.length)
                this.$scope.events.onSelectIngredient(this.$scope.recipeList.list[index]);
            else
                this.$scope.events.onShowMoreRecipe();
        }

        dropDownData.listIngredient.removeClass('selected');
        dropDownData.listSubRecipe.removeClass('selected');
    };

})(app, this);