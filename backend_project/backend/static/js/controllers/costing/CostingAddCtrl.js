/**
 * Created by apium on 30/03/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['$scope', 'CostingAddPresenter', 'CostingAddModel', 'HandsOnTableService'];

    app.controller("CostingAddController", deps.concat([function ($scope, presenter, model, handsOnTableService) {
        CostingAddController.$scope = $scope;
        CostingAddController.presenter = presenter;
        CostingAddController.model = model;
        CostingAddController.handsOnTableService = handsOnTableService;
        return CostingAddController.newInstance();
    }]));

    if (window.define) define(function () {
        return CostingAddController;
    });

    function CostingAddController($scope, presenter, model, handsOnTableService) {
        this.$scope = $scope;
        this.presenter = presenter;
        this.model = model;
        this.handsOnTableService = handsOnTableService;
        this.$scope.events = this.presenter.show(this, this.model);
        this._initFn();
        this.$scope.error = {};
    }

    CostingAddController.newInstance = function ($scope, presenter, model, handsOnTableService) {
        return new CostingAddController(
            $scope || CostingAddController.$scope,
            presenter || CostingAddController.presenter.newInstance(),
            model || CostingAddController.model.newInstance(),
            handsOnTableService || CostingAddController.handsOnTableService.newInstance()
        );
    };

    CostingAddController.prototype._initFn = function () {
        this.$scope.fn = {
            onLoad: this.init.bind(this),
            onSave: this.save.bind(this),
            onChangeGrossPrice: this.setCalculate.bind(this)
        };
    };

    CostingAddController.prototype.showError = function (error) {
        console.log(error);
    };

    CostingAddController.prototype.init = function () {
        var listFamily = this.initCostingFamily();
        $('#costing-modal').on('show.bs.modal', function (e) {
            this.$scope.costing = {
                quantity: 1,
                unit: 'kg',
                grossPrice: '0',
                waste: '0',
                netPrice: '0',
                listFamily: listFamily
            };
            this.$scope.$apply();
            var self = this;
            this.$scope.numberErrorOfTable = false;
            this.$scope.hasDataToAdd = false;
            this.disableAddButton();
            setTimeout(function () {
                self.initTableAddIngredient();
            }, 200);

        }.bind(this))
    };

    CostingAddController.prototype.initCostingFamily = function () {
        var listFamily = ['Meat', 'Spices', 'Eggs', 'Game', 'Pasta', 'Chocolate', 'Grains', 'Rice', 'Poultry',
            'Fruit', 'Vegetables', 'Nuts', 'Legumes', 'Seafood', 'Herbs', 'Dairy', 'Fish', 'Other'];
        listFamily.sort();
        return listFamily;
    };

    CostingAddController.prototype.save = function () {
        var arrData = [];
        for (var row = 0; row < this.$scope.tableAddIngredient.countRows(); row++) {
            if (!this.$scope.tableAddIngredient.isEmptyRow(row)) {
                var data = this.$scope.tableAddIngredient.getDataAtRow(row);
                data = this.decorateData(data);
                arrData.push(data);
            }
        }
        if (arrData.length > 0)
            this.$scope.events.onSave(arrData);
    };

    CostingAddController.prototype.decorateData = function (data) {

        var dataDecorate = {
            ingredient: this.capitalizedFirstLetter(data[0]) || '',
            family: '',
            quantity: data[1] || '',
            unit: data[2] || '',
            grossPrice: data[3] || '',
            waste: data[4] * 100 || '',
            netPrice: this.calculateNetPrice(data[3], data[4]) || 0,
            supplier: '',
            comment: ''
        };
        return dataDecorate;
    };

    CostingAddController.prototype.calculateNetPrice = function (grossPrice, waste) {
        if (isNaN(grossPrice))
            return '0';
        else if (!isNaN(grossPrice)) {
            waste = (isNaN(waste) || waste == null) ? 0 : waste;
            return parseFloat(grossPrice) + (parseFloat(grossPrice) * parseFloat(waste));
        }
    };


    CostingAddController.prototype.validateRow = function () {
        this.$scope.numberErrorOfTable = 0;
        var numberRow = this.$scope.tableAddIngredient.countRows();
        var numberCol = this.$scope.tableAddIngredient.countCols();
        for (var row = 0; row < numberRow; row++) {
            if (this.$scope.tableAddIngredient.isEmptyRow(row)) {
                this.clearEmptyRow(row, numberCol);
            } else {
                for (var col = 0; col < numberCol; col++) {
                    var colHeader = this.$scope.tableAddIngredient.getColHeader(col);
                    switch (colHeader) {
                        case 'Ingredient':
                            this.validateIngredient(row, col);
                            break;
                        case 'Quantity':
                            this.validateQuantity(row, col);
                            break;
                        case 'Units':
                            this.validateUnits(row, col);
                            break;
                        case 'Price':
                            this.validatePrice(row, col);
                            break;
                        case '% Waste':
                            this.validateWaste(row, col);
                            break;
                    }
                }
            }
        }
        if (this.$scope.numberErrorOfTable > 0 || !this.checkTableHasData()) {
            this.disableAddButton();
        } else {
            this.enableAddButton();
        }
    };

    CostingAddController.prototype.disableAddButton = function () {
        $('#btn-add').attr('disabled', true);
        $('#btn-add').addClass('btn-disabled');
    };

    CostingAddController.prototype.enableAddButton = function () {
        $('#btn-add').attr('disabled', false);
        $('#btn-add').removeClass('btn-disabled');
    };

    CostingAddController.prototype.checkTableHasData = function () {
        var rowsEmpty = this.$scope.tableAddIngredient.countEmptyRows();
        var rows = this.$scope.tableAddIngredient.countRows();
        return this.$scope.hasDataToAdd = rowsEmpty < rows;
    };

    CostingAddController.prototype.clearEmptyRow = function (row, numberCol) {
        for (var col = 0; col < numberCol; col++) {
            var cell = $(this.$scope.tableAddIngredient.getCell(row, col));
            cell.removeClass('htInvalid');
        }
    };
    CostingAddController.prototype.validateIngredient = function (row, col) {
        var ingredient = this.$scope.tableAddIngredient.getDataAtCell(row, col);
        var cell = $(this.$scope.tableAddIngredient.getCell(row, col));
        if (ingredient == null || ingredient.trim() == '') {
            this.$scope.numberErrorOfTable++;
            if (!cell.hasClass('htInvalid'))
                cell.addClass('htInvalid');
        }
    };

    CostingAddController.prototype.validateQuantity = function (row, col) {
        var quantity = this.$scope.tableAddIngredient.getDataAtCell(row, col);
        var cell = $(this.$scope.tableAddIngredient.getCell(row, col));
        if (isNaN(quantity) != false) {
            this.$scope.numberErrorOfTable++;
            if (!cell.hasClass('htInvalid'))
                cell.addClass('htInvalid');
        }
    };

    CostingAddController.prototype.validateUnits = function (row, col) {
        var arrUnit = ['kg', 'lbs'];
        var unit = this.$scope.tableAddIngredient.getDataAtCell(row, col);
        var cell = $(this.$scope.tableAddIngredient.getCell(row, col));
        if (unit != null && unit != '' && arrUnit.indexOf(unit) < 0) {
            this.$scope.numberErrorOfTable++;
            if (!cell.hasClass('htInvalid'))
                cell.addClass('htInvalid');
        } else if (unit != null && unit.trim() == '') {
            if (cell.hasClass('htInvalid'))
                cell.removeClass('htInvalid');
        }
    };

    CostingAddController.prototype.validatePrice = function (row, col) {
        var price = this.$scope.tableAddIngredient.getDataAtCell(row, col);
        var cell = $(this.$scope.tableAddIngredient.getCell(row, col));
        if (isNaN(price) != false) {
            this.$scope.numberErrorOfTable++;
            if (!cell.hasClass('htInvalid'))
                cell.addClass('htInvalid');
        }
    };

    CostingAddController.prototype.validateWaste = function (row, col) {
        var wastePercent = this.$scope.tableAddIngredient.getDataAtCell(row, col);
        var cell = $(this.$scope.tableAddIngredient.getCell(row, col));
        if (isNaN(wastePercent) != false) {
            this.$scope.numberErrorOfTable++;
            if (!cell.hasClass('htInvalid'))
                cell.addClass('htInvalid');
        }
    };

    CostingAddController.prototype.saveSuccess = function () {
        window.location.reload(true);
    };

    CostingAddController.prototype.setCalculate = function () {
        var context = {
            grossPrice: this.$scope.costing.grossPrice,
            waste: this.$scope.costing.waste
        };
        this.$scope.events.onChangeCalculateNetPrice(context);
    };

    CostingAddController.prototype.setNetPrice = function (response) {
        this.$scope.error.invalidNetPrice = response.error;
        this.$scope.costing.netPrice = response.netPrice;
    };

    CostingAddController.prototype.initTableAddIngredient = function () {
        var self = this;
        var hotElement = document.querySelector('#addCostingTable');
        var hotSettings = {
            beforeChange: function (changes, source) {
                for (var i = 0; i < changes.length; i++) {
                    var cellChange = changes[i];
                    var col = cellChange[1];
                    var newCellValue = cellChange[3];
                    if (col === "waste" && newCellValue != '' && newCellValue != null) {
                        var hasExhibitionSuffix = new RegExp("%$").test(newCellValue);

                        if (!hasExhibitionSuffix) {
                            newCellValue += "%";
                        }
                        cellChange[3] = numeral().unformat(newCellValue);
                    }

                }
            },
            afterChange: function (changes, source) {
                if (changes && changes.length > 0) {
                    self.validateRow();
                }
            },
            columns: [
                {
                    data: 'ingredient',
                    trimWhiteSpace: true,
                    validator: this.notEmpty,
                },
                {
                    data: 'quantity',
                    type: 'numeric',
                    format: '0.[000]',
                    allowInvalid: true
                }
                ,
                {
                    data: 'unit',
                    type: 'dropdown',
                    source: ['kg', 'lbs']
                }
                ,
                {
                    data: 'price',
                    type: 'numeric',
                    format: '$0.[00]',
                    language: 'en-gb'
                }
                ,
                {
                    data: 'waste',
                    type: 'numeric',
                    format: '0%'
                }
            ],
            startRows: 18,
            stretchH: 'all',
            width: 806,
            autoWrapRow: false,
            height: 480,
            maxRows: 22,
            rowHeaders: true,
            colHeaders: [
                'Ingredient',
                'Quantity',
                'Units',
                'Price',
                '% Waste'
            ]
        };
        this.$scope.tableAddIngredient = this.handsOnTableService.new(hotElement, hotSettings).getTable();
    };
    CostingAddController.prototype.notEmpty = function (value, callback) {
        if (!value || String(value).length === 0 || String(value).trim() == '') {
            callback(false);
        } else {
            callback(true);
        }
    };

    CostingAddController.prototype.capitalizedFirstLetter = function (str) {
        str = str.trim();
        return str.charAt(0).toUpperCase() + str.slice(1);
    };
})(app, this);