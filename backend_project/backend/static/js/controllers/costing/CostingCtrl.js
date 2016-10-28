/**
 * Created by apium on 29/03/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['$scope', 'CostingPresenter', 'CostingModel', 'infrastructure/LocalStorage'];

    app.controller("CostingController", deps.concat([function ($scope, presenter, model, localStorage) {
        CostingController.$scope = $scope;
        CostingController.presenter = presenter;
        CostingController.model = model;
        CostingController.localStorage = localStorage;
        return CostingController.newInstance();
    }]));

    if (window.define) define(function () {
        return CostingController;
    });

    function CostingController($scope, presenter, model, localStorage) {
        this.$scope = $scope;
        this.presenter = presenter;
        this.model = model;
        this.localStorage = localStorage;
        this.$scope.events = this.presenter.show(this, this.model);
        this.USER_TYPE = USER_TYPE;
        this._initFn();
    }

    CostingController.newInstance = function ($scope, presenter, model, localStorage) {
        return new CostingController(
            $scope || CostingController.$scope,
            presenter || CostingController.presenter.newInstance(),
            model || CostingController.model.newInstance(),
            localStorage || CostingController.localStorage.newInstance()
        );
    };

    CostingController.prototype._initFn = function () {
        this.$scope.fn = {
            checkDelete: this.checkDelete.bind(this),
            onDelete: this.onDelete.bind(this),
            onEdit: this.onEdit.bind(this),
            onUpdate: this.onUpdate.bind(this),
            saveWithoutRefresh: this.saveWithoutRefresh.bind(this),
            updateNetPrice: this.updateNetPrice.bind(this),
        };
    };

    CostingController.prototype.init = function (table) {
        this.$scope.costingTable = table;
        this.$scope.isDisabledButton = this.checkUserType();
        this.$scope.isEditting = false;
        this.$scope.listFamily = this.initCostingFamily();
        this.removeLocalStorage();
        this.subcribeOnUpgradeBusiness();
    };

    CostingController.prototype.checkUserType = function () {
        return this.USER_TYPE === 'default' || this.USER_TYPE === 'pro';
    };

    CostingController.prototype.showError = function (error) {
        console.log(error);
    };

    CostingController.prototype.removeLocalStorage = function () {
        this.localStorage.remove('costing_upgrade');
    };

    CostingController.prototype.subcribeOnUpgradeBusiness = function () {
        this.$scope.$on('onUpgradeBusinessPricingModal', function (event, data) {
            this.localStorage.set('costing_upgrade', '/costing/');
        }.bind(this));
    };

    CostingController.prototype.checkDelete = function (ingredient) {
        this.deleteItem = ingredient;
    };

    CostingController.prototype.onDelete = function () {
        var $scope = this.$scope;
        if (this.deleteItem.generic_table_row_id)
            $scope.events.onDeleteGenericItem(this.deleteItem.generic_table_row_id);
        else if (this.deleteItem.custom_id)
            $scope.events.onDeleteCustomItem(this.deleteItem.custom_id);
    };

    CostingController.prototype.deleteSuccess = function () {
        window.location.reload(true);
    };

    CostingController.prototype.reloadPage = function () {
        window.location.reload(true);
    };

    CostingController.prototype.notificationNothing = function (response) {
        this.$scope.editElement.custom_id = response.data.id || this.$scope.editElement.custom_id;
        this.waitingServer = false;
        this.setVariableForEdit();
    };

    CostingController.prototype.onEdit = function (field, element, $index, $event) {
        this.$scope.currentColumn = $($event.currentTarget);
        var currentLine = this.$scope.currentColumn.parents('tr');

        this.$scope.editFieldName = field;
        this.$scope.editIndex = $index;
        this.$scope.element = element;

        if (this.$scope.isEditting && this.$scope.currentLine.attr('class') != currentLine.attr('class')) {
            this.saveWithoutRefresh();
            this.waitingServer = true;
        }

        this.addClassEditToTable();

        if (this.$scope.currentLine != currentLine) {
            this.$scope.currentLine = currentLine;
            this.clearCurrentLine();
            this.$scope.currentLine.addClass('active');
        }
        this.setVariableForEdit();
    };

    CostingController.prototype.addClassEditToTable = function () {
        if (!this.$scope.isEditting) {
            this.$scope.isEditting = true;
            this.$scope.currentColumn.parents('table').addClass('is-editting');
        }
    };


    CostingController.prototype.setVariableForEdit = function () {
        if (this.waitingServer) return false;
        this.$scope.inputAvailable = {};
        this.$scope.inputAvailable[this.$scope.editFieldName] = true;
        this.$scope.inputAvailable.index = this.$scope.editIndex;
        this.$scope.editElement = this.$scope.element;

        var currentColumn = this.$scope.currentColumn;
        setTimeout(function () {
            currentColumn.find('input').focus();
        }, 100);
    };

    CostingController.prototype.onUpdate = function () {
        this.$scope.events.onUpdateIngredientItem(this.$scope.editElement);
    };

    CostingController.prototype.saveWithoutRefresh = function () {
        this.$scope.events.onUpdateIngredientItemWithoutRefresh(this.$scope.editElement);
    };

    CostingController.prototype.clearCurrentLine = function () {
        $('.tblCosting').find('tr').removeClass('active');
    };

    CostingController.prototype.initCostingFamily = function () {
        var listFamily = ['Meat', 'Spices', 'Eggs', 'Game', 'Pasta', 'Chocolate', 'Grains', 'Rice', 'Poultry',
            'Fruit', 'Vegetables', 'Nuts', 'Legumes', 'Seafood', 'Herbs', 'Dairy', 'Fish', 'Other'];
        listFamily.sort();
        return listFamily;
    };

    CostingController.prototype.updateNetPrice = function () {
        this.$scope.editElement.gross_price = this.$scope.editElement.gross_price || 0;
        this.$scope.editElement.waste = this.$scope.editElement.waste || 0;
        this.$scope.editElement.net_price = this.$scope.editElement.gross_price + this.$scope.editElement.gross_price * this.$scope.editElement.waste / 100 || 0;
    };
})(app, this);