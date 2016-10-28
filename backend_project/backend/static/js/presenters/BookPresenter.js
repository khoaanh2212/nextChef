/**
 * Created by apium on 22/03/2016.
 */

;(function(app, window) {
    var deps = ['$timeout'];
    function Factory($timeout) {
        BookPresenter.$timeout = $timeout;
        return BookPresenter;
    }
    app.service('BookPresenter', deps.concat([Factory]));
    if (window.define) define ([], Factory);

    function BookPresenter() {
    }

    BookPresenter.newInstance = function() {
        return new BookPresenter();
    };

    BookPresenter.prototype.show = function(view, model) {
        return {
            onChangeGetCollaborator: this.handleOnChangeGetCollaborator.bind(this, view, model)
        };
    };

    BookPresenter.prototype.handleOnChangeGetCollaborator = function(view, model, name, page) {
        return model.getChefByNameAndLimit(name, page)
            .then(function(response) {
                view.initCollaboratorDropdown(response);
            })
            .catch(view.showError.bind(view));
    };

})(app, this);