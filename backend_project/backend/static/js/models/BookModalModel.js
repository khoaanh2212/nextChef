/**
 * Created by apium on 24/03/2016.
 */
;(function (app, window) {
    var deps = ['Book', 'AjaxService'];

    function Factory(book, AjaxService) {
        BookModalModel.book = book;
        BookModalModel.AjaxService = AjaxService;
        return BookModalModel;
    }

    app.service('BookModalModel', Factory);
    if (window.define) define(Factory);

    Factory.$inject = deps;

    function BookModalModel(book, ajaxService) {
        this.bookObject = book.prototype;
        this.ajaxService = ajaxService;
        this.collaboratorList = [];
        this.collaboratorKeyword = '';
    }

    BookModalModel.newInstance = function (book, ajaxService) {
        ajaxService = ajaxService || BookModalModel.AjaxService.newInstance();
        book = book || BookModalModel.book;
        return new BookModalModel(book, ajaxService);
    };

    BookModalModel.prototype.initModel = function () {
        return {};
    };

    BookModalModel.prototype.createBook = function (context) {
        var body = {
            name: context.name,
            private: context.private,
            collaborators: this._getCollaboratorListAsString(context.collaborators)
        };
        return this.bookObject.addBook(body);
    };

    BookModalModel.prototype._getCollaboratorListAsString = function (collaborators) {
        var ids = collaborators.map(function (c) {
            return c.id
        });
        return ids.join(",");
    };

    BookModalModel.prototype.getChefByNameAndLimit = function (name, page) {
        var self = this;
        this.cleanSearch(name);
        page = page || 1;
        var url = CHEF_GET_BY_NAME_AND_LIMIT + '?chef_name=' + name + '&page_limit=' + page;
        return self.ajaxService.ok('GET', url).then(function (response) {
            return {
                'chefs': self.makeCollaboratorList(response.chefs),
                'readmore': response.readmore
            };
        });
    };

    BookModalModel.prototype.getChefByListId = function (arrId) {
        var self = this;
        var body = {
            arrId: arrId
        };
        var url = CHEF_GET_BY_LIST_ID;
        var requestOption = {timeout: 10000};
        return this.ajaxService.ok('POST', url, body, requestOption).then(function (response) {
            return {
                'chefs': self.makeCollaboratorList(response.chefs),
            };
        });
    };

    BookModalModel.prototype.makeCollaboratorList = function (chefs) {
        this.collaboratorList = this.collaboratorList.concat(chefs);
        return this.collaboratorList;
    };

    BookModalModel.prototype.cleanSearch = function (name) {
        if (this.collaboratorKeyword !== name) {
            this.collaboratorKeyword = name;
            this.collaboratorList = [];
        }
    };

    BookModalModel.prototype.clearCollaboratorsList = function () {
        this.collaboratorList = [];
        return true;
    };

})(app, this);