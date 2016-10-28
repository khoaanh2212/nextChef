/**
 * Created by apium on 24/03/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['PresenterHandlerCreator'];

    app.factory('BookModalPresenter', Factory);

    function Factory(PresenterHandlerCreator) {
        BookModalPresenter.PresenterHandlerCreator = PresenterHandlerCreator;
        return BookModalPresenter;
    }

    Factory.$inject = deps;

    if (window.define) define(Factory);

    function BookModalPresenter(PresenterHandlerCreator) {
        this.Creator = PresenterHandlerCreator;
    }

    BookModalPresenter.prototype.show = function (view, model) {
        var creator = this.Creator.newInstance(this, view, model);
        return {
            onLoad: creator.createEventHandler({
                modelMethod: 'initModel',
                viewSuccess: 'init',
                viewError: 'showError'
            }),
            onClickAddingBook: creator.createEventHandler({
                modelMethod: 'createBook',
                viewSuccess: 'initBookToList',
                viewError: 'showError'
            }),
            onChangeGetCollaborator: creator.createEventHandler({
                modelMethod: 'getChefByNameAndLimit',
                viewSuccess: 'initCollaboratorDropdown'
            }),
            onLoadCollarboratorBeforeEdit: creator.createEventHandler({
                modelMethod: 'getChefByListId',
                viewSuccess: 'initCollaborators'
            }),
            clearCollaboratorsList: creator.createEventHandler({
                modelMethod: 'clearCollaboratorsList',
                viewSuccess: 'showNothing'
            }),
        }
    };

    BookModalPresenter.newInstance = function (PresenterHandlerCreator) {
        return new BookModalPresenter(PresenterHandlerCreator || BookModalPresenter.PresenterHandlerCreator);
    };

})(app, this);