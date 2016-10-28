/**
 * Created by ka on 28/04/2016.
 */
define(function (require) {
    var path = 'controllers/costing/CostingAddCtrl';
    describe(path, function () {
        var controller = require('controllers/costing/CostingAddCtrl');
        var sut, model, view, presenter, $scope, handsonTableService;
        beforeEach(function () {
            window.USER_TYPE = '';
            model = view = $scope = handsonTableService = {};
            presenter = {
                show: function () {
                }
            };
            sut = controller.newInstance($scope, presenter, model, handsonTableService);
            sut.$scope = {
                events: {
                    onSave: jasmine.createSpy(),
                },
                tableAddIngredient: jasmine.createSpy()
            };
        });
        describe('initCostingFamily', function () {
            describe('init Family List', function () {
                it('should return a list family', function () {
                    var expected = ['Chocolate', 'Dairy', 'Eggs', 'Fish', 'Fruit', 'Game', 'Grains', 'Herbs',
                        'Legumes', 'Meat', 'Nuts', 'Other', 'Pasta', 'Poultry', 'Rice', 'Seafood', 'Spices', 'Vegetables'];
                    expect(sut.initCostingFamily()).toEqual(expected);
                });
            });
        });
        describe('decorateData', function () {
            describe('decorate data from table before save', function () {
                it('should return a object decorate', function () {
                    var data = ['ingredient', 3, 'kg', 2, 0.05];
                    sut.calculateNetPrice = jasmine.createSpy().and.returnValue(2.001);
                    var expected = {
                        ingredient: 'Ingredient',
                        family: '',
                        quantity: 3,
                        unit: 'kg',
                        grossPrice: 2,
                        waste: 5,
                        netPrice: 2.001,
                        supplier: '',
                        comment: ''
                    };
                    expect(sut.decorateData(data)).toEqual(expected);
                });
            });
        });

        describe('save', function () {
            describe('save multi ingredient from data table', function () {
                beforeEach(function () {
                    sut.$scope.tableAddIngredient.countRows = jasmine.createSpy().and.returnValue(2);
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(false);
                    sut.$scope.tableAddIngredient.getDataAtRow = jasmine.createSpy().and.returnValue({});
                    sut.decorateData = jasmine.createSpy().and.returnValue({});
                    sut.save();
                });
                it('should call onSave with expected data', function () {
                    expect(sut.$scope.events.onSave).toHaveBeenCalledWith([{}, {}]);
                });
            });
        });
        describe('validateRow', function () {
            describe('when finish edit a cell on table', function () {
                beforeEach(function () {
                    sut.$scope.tableAddIngredient.countRows = jasmine.createSpy().and.returnValue(1);
                    sut.$scope.tableAddIngredient.countCols = jasmine.createSpy().and.returnValue(1);
                    sut.disableAddButton = jasmine.createSpy();
                    sut.enableAddButton = jasmine.createSpy();
                    sut.checkTableHasData = jasmine.createSpy();

                });
                it('should call function clearEmptyRow if row is empty', function () {
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(true);
                    sut.clearEmptyRow = jasmine.createSpy();
                    sut.validateRow();
                    expect(sut.clearEmptyRow).toHaveBeenCalled();
                });
                it('should call function validateIngredient if row not empty column is Ingredient', function () {
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(false);
                    sut.$scope.tableAddIngredient.getColHeader = jasmine.createSpy().and.returnValue('Ingredient');
                    sut.validateIngredient = jasmine.createSpy();
                    sut.validateRow();
                    expect(sut.validateIngredient).toHaveBeenCalled();
                });
                it('should call function validateQuantity if row not empty column is Quantity', function () {
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(false);
                    sut.$scope.tableAddIngredient.getColHeader = jasmine.createSpy().and.returnValue('Quantity');
                    sut.validateQuantity = jasmine.createSpy();
                    sut.validateRow();
                    expect(sut.validateQuantity).toHaveBeenCalled();
                });
                it('should call function validateUnits if row not empty column is Units', function () {
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(false);
                    sut.$scope.tableAddIngredient.getColHeader = jasmine.createSpy().and.returnValue('Units');
                    sut.validateUnits = jasmine.createSpy();
                    sut.validateRow();
                    expect(sut.validateUnits).toHaveBeenCalled();
                });
                it('should call function validatePrice if row not empty column is Price', function () {
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(false);
                    sut.$scope.tableAddIngredient.getColHeader = jasmine.createSpy().and.returnValue('Price');
                    sut.validatePrice = jasmine.createSpy();
                    sut.validateRow();
                    expect(sut.validatePrice).toHaveBeenCalled();
                });
                it('should call function validateWaste if row not empty column is % Waste', function () {
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(false);
                    sut.$scope.tableAddIngredient.getColHeader = jasmine.createSpy().and.returnValue('% Waste');
                    sut.validateWaste = jasmine.createSpy();
                    sut.validateRow();
                    expect(sut.validateWaste).toHaveBeenCalled();
                });
                it('should call function disableAddButton if numberError > 0', function () {
                    sut.$scope.numberErrorOfTable = 1;
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(false);
                    sut.$scope.tableAddIngredient.getColHeader = jasmine.createSpy().and.returnValue('What ever');
                    sut.checkTableHasData = jasmine.createSpy().and.returnValue(false);
                    sut.validateRow();
                    expect(sut.disableAddButton).toHaveBeenCalled();
                });
                it('should call function disableAddButton if checkTableHasData = false', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(false);
                    sut.$scope.tableAddIngredient.getColHeader = jasmine.createSpy().and.returnValue('What ever');
                    sut.checkTableHasData = jasmine.createSpy().and.returnValue(false);
                    sut.validateRow();
                    expect(sut.disableAddButton).toHaveBeenCalled();
                });
                it('should call function enableButton if checkTableHasData = true and numberError = 0', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.isEmptyRow = jasmine.createSpy().and.returnValue(false);
                    sut.$scope.tableAddIngredient.getColHeader = jasmine.createSpy().and.returnValue('What ever');
                    sut.checkTableHasData = jasmine.createSpy().and.returnValue(true);
                    sut.validateRow();
                    expect(sut.enableAddButton).toHaveBeenCalled();
                });
            });
        });

        describe('checkTableHasData', function () {
            describe('when empty row smaller than all row of table', function () {
                it('should return true', function () {
                    sut.$scope.tableAddIngredient.countEmptyRows = jasmine.createSpy().and.returnValue(4);
                    sut.$scope.tableAddIngredient.countRows = jasmine.createSpy().and.returnValue(5);
                    expect(sut.checkTableHasData()).toEqual(true);

                });
            });
            describe('when empty row equal row of table', function () {
                it('should return false', function () {
                    sut.$scope.tableAddIngredient.countEmptyRows = jasmine.createSpy().and.returnValue(5);
                    sut.$scope.tableAddIngredient.countRows = jasmine.createSpy().and.returnValue(5);
                    expect(sut.checkTableHasData()).toEqual(false);
                });
            });
        });

        describe('validateIngredient', function () {
            describe('when ingredient is null', function () {
                it('should increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue(null);
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validateIngredient('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(1);
                });
            });
            describe('when ingredient is blank', function () {
                it('should increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue('');
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validateIngredient('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(1);
                });
            });
            describe('when ingredient is correct', function () {
                it('should not increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue('what ever');
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validateIngredient('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(0);
                });
            });
        });
        describe('validateQuantity', function () {
            describe('when quantity is not a number', function () {
                it('should increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue('aaaaa');
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validateQuantity('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(1);
                });
            });
            describe('when quantity is a number', function () {
                it('should not increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue(99);
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validateQuantity('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(0);
                });
            });
        });
        describe('validateUnits', function () {
            describe('when unit not in array [kg,lbs]', function () {
                it('should increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue('what ever');
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validateUnits('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(1);
                });
            });
            describe('when unit in array [kg,lbs]', function () {
                it('should not increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue('kg');
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validateUnits('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(0);
                });
            });
        });
        describe('validatePrice', function () {
            describe('when price is not a number', function () {
                it('should increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue('what ever');
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validatePrice('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(1);
                });
            });
            describe('when price is a number', function () {
                it('should not increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue(99);
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validatePrice('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(0);
                });
            });
        });
        describe('validateWaste', function () {
            describe('when waste is not a number', function () {
                it('should increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue('what ever');
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validateWaste('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(1);
                });
            });
            describe('when waste is a number', function () {
                it('should not increase numberError', function () {
                    sut.$scope.numberErrorOfTable = 0;
                    sut.$scope.tableAddIngredient.getDataAtCell = jasmine.createSpy().and.returnValue(99);
                    sut.$scope.tableAddIngredient.getCell = jasmine.createSpy().and.returnValue({});
                    sut.validateWaste('', '');
                    expect(sut.$scope.numberErrorOfTable).toEqual(0);
                });
            });
        });

        describe('capitalizedFirstLetter', function () {
            describe('when first letter is normal char', function () {
                it('should return string with first letter uppercase', function () {
                    expect(sut.capitalizedFirstLetter('apple')).toEqual('Apple');
                });
            });
            describe('when first letter is not normal char', function () {
                it('should return nothing change string', function () {
                    expect(sut.capitalizedFirstLetter('/apple')).toEqual('/apple');
                });
            });
        });

        describe('calculateNetPrice', function () {
            it('should return 0 if gross price or waste not a number', function () {
                expect(sut.calculateNetPrice('what ever', '20')).toEqual('0');
            });
            it('should return expect value when gross price and waste are numbers', function () {
                expect(sut.calculateNetPrice('100', '0.1')).toEqual(110);
            });
        });
    });

});