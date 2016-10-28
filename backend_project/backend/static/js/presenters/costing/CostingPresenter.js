/**
 * Created by apium on 24/03/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['PresenterHandlerCreator'];

    app.factory('CostingPresenter', Factory);

    function Factory(PresenterHandlerCreator) {
        CostingPresenter.PresenterHandlerCreator = PresenterHandlerCreator;
        return CostingPresenter;
    }

    Factory.$inject = deps;

    if (window.define) define(Factory);

    function CostingPresenter(PresenterHandlerCreator) {
        this.Creator = PresenterHandlerCreator;
    }

    CostingPresenter.prototype.show = function (view, model) {
        var creator = this.Creator.newInstance(this, view, model);
        return {
            onLoad: creator.createEventHandler({
                modelMethod: 'getCostingTable',
                viewSuccess: 'init',
                viewError: 'showError'
            }),
            onDeleteGenericItem: creator.createEventHandler({
                modelMethod: 'deleteGenericItem',
                viewSuccess: 'deleteSuccess',
                viewError: 'showError'
            }),
            onDeleteCustomItem: creator.createEventHandler({
                modelMethod: 'deleteCustomItem',
                viewSuccess: 'deleteSuccess',
                viewError: 'showError'
            }),
            onDuplicate: creator.createEventHandler({
                modelMethod: 'duplicate',
                viewSuccess: 'init',
                viewError: 'showError'
            }),
            onUpdateIngredientItem: creator.createEventHandler({
                modelMethod: 'updateIngredientItem',
                viewSuccess: 'reloadPage',
                viewError: 'showError'
            }),
            onUpdateIngredientItemWithoutRefresh: creator.createEventHandler({
                modelMethod: 'updateIngredientItem',
                viewSuccess: 'notificationNothing',
                viewError: 'showError'
            })
        }
    };

    CostingPresenter.newInstance = function (PresenterHandlerCreator) {
        return new CostingPresenter(PresenterHandlerCreator || CostingPresenter.PresenterHandlerCreator);
    };

})(app, this);