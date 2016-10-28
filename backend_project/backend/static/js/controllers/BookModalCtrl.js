/**
 * Created by apium on 24/03/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['$scope', 'BookModalPresenter', 'BookModalModel', '$timeout', '$http'];

    app.controller("BookModalController", deps.concat([function ($scope, presenter, model, $timeout, $http) {
        BookModalController.$scope = $scope;
        BookModalController.presenter = presenter;
        BookModalController.model = model;
        BookModalController.$timeout = $timeout;
        BookModalController.$http = $http;
        return BookModalController.newInstance();
    }]));

    if (window.define) define(function () {
        return BookModalController;
    });

    function BookModalController($scope, presenter, model, $timeout, $http) {
        this.$scope = $scope;
        this.presenter = presenter;
        this.model = model;
        this.$timeout = $timeout;
        this.$http = $http;
        this.$scope.events = this.presenter.show(this, this.model);

        this.$scope.onClickAddingBook = this.onClickAddingBook.bind(this);

        this._initFn();

        $scope.range = function (min, max, step) {
            step = step || 1;
            var input = [];
            for (var i = min; i <= max; i += step) {
                input.push(i);
            }
            return input;
        };
    }

    BookModalController.prototype.subscribeEditBook = function () {
        this.$scope.$on('broadcast_edit_book', function (event, args) {
            this.$scope.bookEdit = args.editBook;
            this.saveOldBook(this.$scope.bookEdit);
            this.assignBookToEdit(args.editBook);
        }.bind(this));
    };

    BookModalController.prototype.subscribeAddBook = function () {
        this.$scope.$on('broadcast_add_book', function (event, args) {
            this.$scope.isCreate = true;
            this.$scope.book = {
                name: '',
                private: 0,
                collaborators: []
            };
        }.bind(this));
    };

    BookModalController.prototype.saveOldBook = function (book) {
        this.$scope.oldBook = {
            name: book.name,
            private: book.private,
            collaborators: book.collaborators
        }
    };

    BookModalController.prototype.assignBookToEdit = function (book) {
        var collaborators = book.collaborators;
        book.collaborators = [];
        this.$scope.book = book;
        // var arrCollaborators = collaborators == '' ? [] : this.decorateCollaborators(collaborators);
        var arrCollaborators = collaborators == '' ? [] : this.decorateCollaborators(collaborators);
        this.loadEditCollaborators(arrCollaborators);
    };

    BookModalController.prototype.loadEditCollaborators = function (arrCollaborators) {
        if (arrCollaborators.length > 0)
            this.$scope.events.onLoadCollarboratorBeforeEdit(arrCollaborators);
    };

    BookModalController.newInstance = function ($scope, presenter, model, $timeout, $http) {
        return new BookModalController(
            $scope || BookModalController.$scope,
            presenter || BookModalController.presenter.newInstance(),
            model || BookModalController.model.newInstance(),
            $timeout || BookModalController.$timeout,
            $http || BookModalController.$http
        );
    };

    BookModalController.prototype._initFn = function () {
        this.$scope.fn = {
            loadMoreCollaborator: this.loadMoreCollaborator.bind(this),
            getCollaborator: this.getCollaborator.bind(this),
            selectCollaborator: this.selectCollaborator.bind(this),
            onCancelEdit: this.cancelEdit.bind(this),
            onUpdateBook: this.updateBook.bind(this)
        };
    };

    BookModalController.prototype.init = function () {
        this.$scope.bookEdit = {};
        this.$scope.isUpdate = false;
        this.$scope.isCreate = false;
        this.$scope.book = {
            name: '',
            private: 0,
            collaborators: []
        };
        this.subscribeEditBook();
        this.subscribeAddBook();
        this.initDefaultModal();

    };

    BookModalController.prototype.initDefaultModal = function () {
        var self = this;
        $('#book_modal').on('show.bs.modal', function (e) {
            self.$scope.book = {
                name: self.$scope.book.name,
                private: self.$scope.book.private,
                collaborators: self.$scope.book.collaborators
            };
            if (!self.$scope.$$phase) self.$scope.$apply();
        });
        $('#book_modal').on('hide.bs.modal', function (e) {
            if (!this.$scope.isUpdate && !this.$scope.isCreate)
                self.cancelEdit();
            else if (this.$scope.isCreate)
                this.$scope.isCreate = false;

        }.bind(this));
    };

    BookModalController.prototype.showError = function (error) {
        console.log(error);
    };

    BookModalController.prototype.showNothing = function () {
    };

    BookModalController.prototype.initBookToList = function (response) {
        this.$scope.$emit('addingBookToSlide', response.data);
    };

    BookModalController.prototype.onClickAddingBook = function () {
        this.$scope.events.onClickAddingBook(this.$scope.book);
    };

    BookModalController.prototype.getCollaborator = function (name) {
        var self = this;
        var $scope = self.$scope;
        // Because using old angular version 1.2.0, not support debounce, we using timeout.

        if (self._timeout) {
            self.$timeout.cancel(self._timeout);
        }
        self._timeout = self.$timeout(function () {
            if (name === '') {
                $scope.isShowCollaboratorDropdown = false;
            } else {
                $scope.events.onChangeGetCollaborator(name);
            }
            self._timeout = null;
        }, 800);
    };

    BookModalController.prototype.initCollaboratorDropdown = function (response) {
        var $scope = this.$scope;
        $scope.collaborators = $scope.collaborators || {};
        $scope.collaborators.chefs = response.chefs;
        $scope.collaborators.readmore = response.readmore;
        $scope.isShowCollaboratorDropdown = true;
        $scope.collaboratorDropdownPaging = $scope.collaboratorDropdownPaging || 1;
    };

    BookModalController.prototype.initCollaborators = function (response) {
        this.$scope.book.collaborators = response.chefs;
    };

    BookModalController.prototype.loadMoreCollaborator = function (name, page) {
        var $scope = this.$scope;
        $scope.collaboratorDropdownPaging = page + 1;
        $scope.events.onChangeGetCollaborator(name, $scope.collaboratorDropdownPaging);
    };

    BookModalController.prototype.selectCollaborator = function (collaborator) {
        var $scope = this.$scope;
        if (!this._isCollaboratorSelected(collaborator))
            $scope.book.collaborators.push(collaborator);
        $scope.isShowCollaboratorDropdown = false;
        $scope.colaborator_name = undefined;
    };

    BookModalController.prototype._isCollaboratorSelected = function (collaborator) {
        var $scope = this.$scope;
        return $scope.book.collaborators.some(function (c) {
            return c.email === collaborator.email;
        });
    };

    BookModalController.prototype.decorateCollaborators = function (strCollaborators) {
        strCollaborators = this.replaceAll(strCollaborators, '[', '');
        strCollaborators = this.replaceAll(strCollaborators, ']', '');
        var length = strCollaborators.length;
        if (strCollaborators[length - 1] == ',') {
            strCollaborators = strCollaborators.substr(0, length - 1);
        }
        var arrCollaborators = strCollaborators.split(',');
        for (var i = 0; i < arrCollaborators.length; i++) {
            arrCollaborators[i] = parseInt(arrCollaborators[i]);
        }
        return arrCollaborators;
    };

    BookModalController.prototype.replaceAll = function (target, search, replacement) {
        while (target.indexOf(search) != -1) {
            target = target.replace(search, replacement);
        }
        return target;
    };

    BookModalController.prototype.cancelEdit = function () {
        this.decorateCollaboratorsBeforeCancel();
        this.$scope.$emit('emit_cancel_edit_book', {book: this.$scope.bookEdit});
        this.$scope.events.clearCollaboratorsList();
    };

    BookModalController.prototype.updateBook = function () {
        this.decorateCollaboratorsBeforeUpdate();
        this.$scope.$emit('emit_update_book', {book: this.$scope.bookEdit});
        this.$scope.events.clearCollaboratorsList();
    };

    BookModalController.prototype.decorateCollaboratorsBeforeUpdate = function () {
        var strCollaborators = '';
        var bookCollaborators = this.$scope.book.collaborators;
        for (var i = 0; i < bookCollaborators.length; i++) {
            if (strCollaborators == '')
                strCollaborators = strCollaborators + '[' + bookCollaborators[i].id + ']';
            else
                strCollaborators = strCollaborators + ',[' + bookCollaborators[i].id + ']';
        }
        this.$scope.bookEdit.collaborators = strCollaborators;
        this.$scope.bookEdit.name = this.$scope.book.name;
        this.$scope.bookEdit.private = this.$scope.book.private;

    };
    BookModalController.prototype.decorateCollaboratorsBeforeCancel = function () {
        this.$scope.bookEdit.collaborators = this.$scope.oldBook.collaborators;
        this.$scope.bookEdit.name = this.$scope.oldBook.name;
        this.$scope.bookEdit.private = this.$scope.oldBook.private;
    };
})(app, this);