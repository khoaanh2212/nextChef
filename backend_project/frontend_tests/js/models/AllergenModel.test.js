/**
 * Created by Kate on 3/23/16.
 */

define(function (require) {

    var path = 'models/AllergenModel';
    describe(path, function () {

        var AllergenModel = require('models/AllergenModel');
        var PromiseHelper = require('../../test-helpers/Promise.js');

        var sut;

        beforeEach(function () {
            ajaxService = {};
            sut = AllergenModel.newInstance(ajaxService);
        });

        describe('onEdamamAnalyze', function () {

            beforeEach(function () {
                var ingredient_list = [
                    {name: 'A'}, {name: 'B'}
                ];
                window.EDAMAM_URL = 'edamam_url';
                sut.ajaxService.ok = jasmine.createSpy().and.returnValue(PromiseHelper.fake([]));
                sut.onEdamamAnalyze(ingredient_list);
            });

            it('should call once to the ajax service', function () {
                expect(sut.ajaxService.ok.calls.count()).toBe(1)
            });

            it('should call the ajax service with parameters', function () {

                var expectedData = ['A', 'B'];
                var expectedOptions = {timeout: 10000};
                var expectedUrl = 'edamam_url';
                var expectedMethod = 'POST';

                expect(sut.ajaxService.ok.calls.allArgs()).toEqual([
                    [expectedMethod, expectedUrl, expectedData, expectedOptions]
                ]);
            });
        });

        describe('_decorateEdamamRequest', function () {

            it('should return the expected list of ingredients', function () {
                var input = [
                    {
                        "id": "ingredients0",
                        "name": "RECIPE SUBTEST",
                        "linkRecipeId": "40",
                        "subIngredients": [
                            {
                                "id": 560,
                                "name": "milk"
                            },
                            {
                                "id": 561,
                                "name": "salmon"
                            }, {
                                "id": 562,
                                "name": "peanut butter"
                            }]
                    },
                    {
                        "id": "ingredients1",
                        "name": "fish",
                        "linkRecipeId": null
                    }
                ];

                var expected = [
                    'RECIPE SUBTEST', 'milk', 'salmon', 'peanut butter', 'fish'
                ];

                var actual = sut._decorateEdamamRequest(input);
                expect(actual).toEqual(expected);

            });

        });

    });
});