/**
 * Created by Kate on 3/22/16.
 */
define(function (require) {

    describe('AllergenOnKitchenController', function () {

        var AllergenOnKitchenController = require('controllers/AllergenOnKitchenCtrl');

        var sut, toaster = {}, model = {}, presenter = {
            show: function () {
            }
        };

        var $scope = {
            $on: jasmine.createSpy()
        };

        beforeEach(function () {
            window.ALL_ALLERGENS = ['nut', 'fish', 'egg'];
            sut = AllergenOnKitchenController.newInstance($scope, model, presenter, toaster);
            sut.events = {};
        });

        describe('fn', function () {
            var expected = ['toggleAllergen'];
            describe('always', function () {
                it('should define expected properties in fn', function () {
                    var actual = Object.keys(sut.fn);
                    expect(actual).toEqual(expected);
                });

                it('should define only functions', function () {
                    var fn = sut.fn;
                    Object.keys(fn).forEach(function (key) {
                        expect(typeof fn[key]).toBe('function');
                    });
                });
            });
        });

        describe('onLoad', function () {
            describe('invalid input', function () {
                var testCases = ['', undefined];
                testCases.forEach(function (test) {
                    it('should throw if saved_allergens is invalid', function () {
                        expect(function () {
                            sut.onLoad(test)
                        }).toThrow(new Error('Saved allergens list cannot be empty'));
                    })
                });
            });

            describe('valid input', function () {
                var testCases = [[], ['fish']];
                testCases.forEach(function (test) {
                    it('should not throw if saved_allergens is valid', function () {
                        expect(function () {
                            sut.onLoad(test)
                        }).not.toThrow();
                    })
                });

                it('should assign the saved_allergens to allergens', function () {
                    sut.allergens = undefined;
                    sut.onLoad(['fish']);
                    expect(sut.allergens).toEqual(['fish']);
                });

                it('should assign init the selectedAllergens list', function () {
                    sut.data = {selectedAllergens: {}};
                    sut.onLoad(['fish']);
                    expect(sut.data.selectedAllergens).toEqual({'fish': true});
                });

            });

        });

        describe('toggleAllergen', function () {

            var index = 1, recipe = {};

            beforeEach(function () {
                sut.updateAllergenForRecipe = jasmine.createSpy();
                sut.allergens = [];
            });

            it('should add allergen to allergens list if does not exist', function () {
                sut.allergens = [];
                sut.data.allergensList = ['fish', 'nut', 'celery'];
                sut.toggleAllergen(index, recipe);
                expect(sut.allergens).toEqual(['nut']);
            });

            it('should remove allergen to allergens list if exist', function () {
                sut.allergens = ['nut'];
                sut.data.allergensList = ['fish', 'nut', 'celery'];
                sut.toggleAllergen(index, recipe);
                expect(sut.allergens).toEqual([]);
            });

            it('should call to updateAllergenForRecipe', function () {
                sut.updateAllergenForRecipe = jasmine.createSpy();
                sut.toggleAllergen(index, recipe);
                expect(sut.updateAllergenForRecipe).toHaveBeenCalled();
            });

        });

        describe('updateAllergenForRecipe', function () {

            describe('always', function () {
                beforeEach(function () {
                    sut.previous_allergens = sut.allergens = [];
                    sut.$scope = {
                        recipe: {
                            editAllergen: jasmine.createSpy()
                        }
                    }
                });

                it('should not throw', function () {
                    expect(function () {
                        sut.updateAllergenForRecipe()
                    }).not.toThrow();
                });

                it('should assign allergen to recipe', function () {
                    sut.allergens = [];
                    sut.updateAllergenForRecipe();
                    expect(sut.$scope.recipe.allergen = []);
                });

                it('should assign deleted_allergen to recipe', function () {
                    sut._getDeletedAllergens = jasmine.createSpy().and.returnValue([]);
                    sut.updateAllergenForRecipe();
                    expect(sut.$scope.recipe.deleted_allergens = []);
                });

                it('should assign added_allergens to recipe', function () {
                    sut._getAddedAllergens = jasmine.createSpy().and.returnValue([]);
                    sut.updateAllergenForRecipe();
                    expect(sut.$scope.recipe.added_allergens = []);
                });

                it('should call editAllergen function from recipe', function () {
                    sut.updateAllergenForRecipe();
                    expect(sut.$scope.recipe.editAllergen).toHaveBeenCalled();
                })
            })

        });

        describe('onIngredientAdded', function () {

            var result = ['fish', 'celery', 'egg'];

            beforeEach(function () {
                sut.toaster = {
                    sendAlert: jasmine.createSpy()
                };
                sut.events.onUpdateAllergen = jasmine.createSpy();
                sut.$scope.recipe = {
                    id: 1
                };
                sut.onIngredientAdded();
            });

            it('should update the allergen', function() {
                expect(sut.events.onUpdateAllergen).toHaveBeenCalledWith(1);
            });

        });

        describe('onAllergenLoaded', function() {

            var oldList = ['fish'];
            var newList = ['nut', 'egg'];

            beforeEach(function() {
                sut.data.selectedAllergens = {
                    'fish': true,
                    'nut': false,
                    'egg': false
                };
                sut.allergens = oldList;
                sut.onAllergenLoaded(newList);
            });

            it('should update the allergens', function() {
                expect(sut.allergens).toEqual(newList);
                expect(sut.data.selectedAllergens).toEqual({
                    'fish': false,
                    'nut': true,
                    'egg': true
                });
            });

        });

        describe('_getDeletedAllergens', function() {
            describe('when some elements are deleted', function() {
                it('should return the deleted allergens', function() {
                    current = ['a', 'b', 'd', 'e'];
                    previous = ['a', 'c', 'd', 'f'];
                    actual = sut._getDeletedAllergens(previous, current);
                    expect(actual).toEqual(['c', 'f'])
                })
            });
            describe('when no element is deleted', function() {
                it('should return empty array', function() {
                    current = ['a', 'b', 'd', 'e'];
                    previous = [];
                    actual = sut._getDeletedAllergens(previous, current);
                    expect(actual).toEqual([])
                })
            });
        });

        describe('_getAddedAllergens', function() {
            describe('when some elements are added', function() {
                it('should return the added allergens', function() {
                    current = ['a', 'b', 'd', 'e'];
                    previous = ['a', 'c', 'd', 'f'];
                    actual = sut._getAddedAllergens(previous, current);
                    expect(actual).toEqual(['b', 'e'])
                })
            });
            describe('when no element is added', function() {
                it('should return empty array', function() {
                    current = ['a', 'd', 'e'];
                    previous = ['a', 'b', 'd', 'e'];
                    actual = sut._getAddedAllergens(previous, current);
                    expect(actual).toEqual([])
                })
            });
        });

    });

});