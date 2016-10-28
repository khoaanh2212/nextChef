/**
 * Created by apium on 22/03/2016.
 */
;(function(app, window) {
    var deps = ['Chef'];
    function Factory(chefModel) {
        BookModel.chefModel = chefModel;
        return BookModel;
    }
    app.service('BookModel', deps.concat([Factory]));
    if (window.define) define (['../models/Chef'], Factory);

    function BookModel(chefModel) {
        this.chefModel = chefModel;
        this.collaboratorList = [];
        this.collaboratorKeyword = '';
    }

    BookModel.newInstance = function(chefModel) {
        return new BookModel(chefModel || BookModel.chefModel);
    };

    BookModel.prototype.getChefByNameAndLimit = function(name, page) {
        this.cleanSearch(name);
        return this.chefModel.getChefByNameLimit(name, page)
            .then(function(response) {
                return {
                    'chefs': this.makeCollaboratorList(response.data.chefs),
                    'readmore': response.data.readmore
                };
            }.bind(this));
    };

    BookModel.prototype.makeCollaboratorList = function(chefs) {
        this.collaboratorList = this.collaboratorList.concat(chefs);
        return this.collaboratorList;
    };

    BookModel.prototype.cleanSearch = function(name) {
        if (this.collaboratorKeyword !== name) {
            this.collaboratorKeyword = name;
            this.collaboratorList = [];
        }
    };

})(app, this);