/**
 * Created by apium on 07/04/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['PresenterHandlerCreator'];

    app.factory('IngredientDetailPresenter', Factory);

    function Factory(PresenterHandlerCreator) {
        IngredientDetailPresenter.PresenterHandlerCreator = PresenterHandlerCreator;
        return IngredientDetailPresenter;
    }

    Factory.$inject = deps;

    if (window.define) define(Factory);

    function IngredientDetailPresenter(PresenterHandlerCreator) {
        this.Creator = PresenterHandlerCreator;
    }

    IngredientDetailPresenter.prototype.show = function (view, model) {
        var creator = this.Creator.newInstance(this, view, model);
        return {
            onLoad: creator.createEventHandler({
                modelMethod: 'initModel',
                viewSuccess: 'init',
                viewError: 'showError'
            })
        }
    };

    IngredientDetailPresenter.newInstance = function (PresenterHandlerCreator) {
        return new IngredientDetailPresenter(PresenterHandlerCreator || IngredientDetailPresenter.PresenterHandlerCreator);
    };

})(app, this);