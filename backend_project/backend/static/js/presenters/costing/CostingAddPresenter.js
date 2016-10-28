/**
 * Created by apium on 24/03/2016.
 */
;(function(app, window) {
    'use strict';

    var deps = ['PresenterHandlerCreator'];

    app.factory('CostingAddPresenter', Factory);

    function Factory(PresenterHandlerCreator) {
        CostingAddPresenter.PresenterHandlerCreator = PresenterHandlerCreator;
        return CostingAddPresenter;
    }

    Factory.$inject = deps;

    if (window.define) define(Factory);

    function CostingAddPresenter(PresenterHandlerCreator) {
        this.Creator = PresenterHandlerCreator;
    }

    CostingAddPresenter.prototype.show = function(view, model) {
        var creator = this.Creator.newInstance(this, view, model);
        return {
            onSave: creator.createEventHandler({
                modelMethod: 'save',
                viewSuccess: 'saveSuccess',
                viewError: 'showError'
            }),
            onChangeCalculateNetPrice: creator.createEventHandler({
                modelMethod: 'calculateNetPrice',
                viewSuccess: 'setNetPrice',
                viewError: 'showError'
            })
        }
    };

    CostingAddPresenter.newInstance = function(PresenterHandlerCreator) {
        return new CostingAddPresenter(PresenterHandlerCreator || CostingAddPresenter.PresenterHandlerCreator);
    };

})(app, this);