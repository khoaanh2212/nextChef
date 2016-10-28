/**
 * Created by apium on 01/04/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['PresenterHandlerCreator'];

    app.factory('IngredientPresenter', Factory);

    function Factory(PresenterHandlerCreator) {
        IngredientPresenter.PresenterHandlerCreator = PresenterHandlerCreator;
        return IngredientPresenter;
    }

    Factory.$inject = deps;

    if (window.define) define(Factory);

    function IngredientPresenter(PresenterHandlerCreator) {
        this.Creator = PresenterHandlerCreator;
    }

    IngredientPresenter.prototype.show = function (view, model) {
        var creator = this.Creator.newInstance(this, view, model);
        return {
            onLoad: creator.createEventHandler({
                modelMethod: 'getIngredientList',
                viewSuccess: 'init',
                viewError: 'showError'
            }),
            onUpdateRecipe: creator.createEventHandler({
                modelMethod: 'getIngredientList',
                viewSuccess: 'onUpdateRecipeDetails',
                viewError: 'showError'
            }),
            getIngredientList: creator.createEventHandler({
                modelMethod: 'makeDropdownList',
                viewSuccess: 'showDropdownList',
                viewError: 'showError'
            }),
            onSelectIngredient: creator.createEventHandler({
                modelMethod: 'makeSelectedIngredient',
                viewSuccess: 'executeSelectedIngredient',
                viewError: 'showError'
            }),
            onShowMoreIngredient: creator.createEventHandler({
                modelMethod: 'getMoreIngredient',
                viewSuccess: 'showDropdownList',
                viewError: 'showError'
            }),
            onShowMoreRecipe: creator.createEventHandler({
                modelMethod: 'getMoreRecipe',
                viewSuccess: 'showDropdownList',
                viewError: 'showError'
            }),
            onAddingIngredient: creator.createEventHandler({
                modelMethod: 'validateAdding',
                viewSuccess: 'addSuccess',
                viewError: 'toasterError'
            }),
            onDeleteIngredient: creator.createEventHandler({
                modelMethod: 'validateDelete',
                viewSuccess: 'deleteSuccess',
                viewError: 'showError'
            }),
            onClearSelectedIngredient: creator.createEventHandler({
                modelMethod: 'clearSelectedIngredient',
                viewSuccess: 'returnEmpty',
                viewError: 'returnEmpty'
            }),
        }
    };

    IngredientPresenter.newInstance = function (PresenterHandlerCreator) {
        return new IngredientPresenter(PresenterHandlerCreator || IngredientPresenter.PresenterHandlerCreator);
    };

})(app, this);