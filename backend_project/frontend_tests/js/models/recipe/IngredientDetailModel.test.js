/**
 * Created by apium on 05/04/2016.
 */
define(function (require) {
    var path = 'models/recipe/IngredientDetailModel';
    describe(path, function () {
        var Model = require('models/recipe/IngredientDetailModel');
        var PromiseHelper = require('../../../test-helpers/Promise.js');

        var sut;
        beforeEach(function () {
            sut = Model.newInstance();
            sut.$http = {};
            sut.$q = {};
            window.RECIPE_ID = 1;
        });

        describe('initModel', function() {
            var actual;
            beforeEach(function() {
                window.SERVINGS = 10;
                var response = {data: {ingredients: [
                    { price: '1' },
                    { price: '1' }
                ]}};
                sut.$http.get = jasmine.createSpy().and.returnValue(PromiseHelper.fake(response));
                actual = sut.initModel();
            });

            it('should call to backend', function() {
                expect(sut.$http.get).toHaveBeenCalled();
            });

            it('should calculate total', function() {
                expect(sut.total).toBe(2);
            });

            it('should return value', function() {
                var expected = {
                    ingredients: [{ price: '1' }, { price: '1' }],
                    total: 2,
                    totalCostPerPortion: 0.2,
                    grossProfit: 0.6,
                    foodCost: 0.2,
                    singlePortion: 0.8,
                    VAT: 0.96,
                    hasEmptyIngredient: false
                };
                expect(actual.getActualResult()).toEqual(expected);
            });
        });

    });
});