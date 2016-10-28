/**
 * Created by khoaanh on 01/06/2016.
 */
define(function (require) {
    describe('IngredientDetailController', function () {
        var IngredientDetailController = require('controllers/recipe/IngredientDetailCtrl');
        var sut, model = {}, presenter = {
            show: function () {

            }
        };
        var $scope = {
            $on: jasmine.createSpy()
        };
        beforeEach(function () {
            sut = IngredientDetailController.newInstance($scope, presenter, model);
            $scope.events = {};
        });
        describe('fn', function () {
            var expected = ['linkRecipe', 'publishGrossProfitEvent', 'publishFoodCostEvent', 'publishVatEvent', 'publishServings'];
            describe('always', function () {
                it('should define expected properties in fn', function () {
                    var actual = Object.keys(sut.$scope.fn);
                    expect(actual).toEqual(expected);
                });
                it('should define only function', function () {
                    var fn = sut.$scope.fn;
                    Object.keys(fn).forEach(function (key) {
                        expect(typeof fn[key]).toBe('function');
                    });
                });
            });
        });
        describe('handleListIngredientAfterChangeServings', function () {
            describe('when old servings and new servings are different', function () {
                it('should recalculate price and quantity', function () {
                    sut.$scope.ingredientList = [{price: 50, quantity: 1}, {price: 60, quantity: 2}];
                    sut.$scope.oldServings = 8;
                    sut.$scope.servings = 4;
                    var expected = [{price: 25, quantity: 0.5}, {price: 30, quantity: 1}];
                    sut.handleListIngredientAfterChangeServings()
                    expect(sut.$scope.ingredientList).toEqual(expected);
                });
            });
        });
    });
});