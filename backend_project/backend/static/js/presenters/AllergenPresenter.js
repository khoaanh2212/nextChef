/**
 * Created by Kate on 3/23/16.
 */
;(function(app, window) {
    'use strict';

    var deps = ['PresenterHandlerCreator'];

    app.factory('AllergenPresenter', Factory);

    function Factory(PresenterHandlerCreator) {
        AllergenPresenter.PresenterHandlerCreator = PresenterHandlerCreator;
        return AllergenPresenter;
    }

    Factory.$inject = deps;

    if (window.define) define(Factory);

    function AllergenPresenter(PresenterHandlerCreator) {
        this.Creator = PresenterHandlerCreator;
    }

    AllergenPresenter.prototype.show = function(view, model) {
        var creator = this.Creator.newInstance(this, view, model);
        return {
            onUpdateAllergen: creator.createEventHandler({
                modelMethod: 'loadAllergen',
                viewSuccess: 'onAllergenLoaded',
                viewError: 'showError'
            })
        }
    };

    AllergenPresenter.newInstance = function(PresenterHandlerCreator) {
        return new AllergenPresenter(PresenterHandlerCreator || AllergenPresenter.PresenterHandlerCreator);
    };

})(app, this);