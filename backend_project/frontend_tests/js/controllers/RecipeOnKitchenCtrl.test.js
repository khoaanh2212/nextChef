/**
 * Created by Kate on 3/22/16.
 */
define(function (require) {

    describe('RecipeOnKitchenController', function () {

        var RecipeOnKitchenController = require('controllers/RecipeOnKitchenCtrl');

        var sut, $scope = {};

        beforeEach(function () {
            $scope = {
                publish: jasmine.createSpy(),
                recipe: {}
            };
            sut = RecipeOnKitchenController.newInstance($scope);
        });

        describe('fn', function () {
            var expected = ['savePublic', 'savePrivate'];
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

        describe('savePublic', function() {
            beforeEach(function() {
                sut.savePublic();
            });
            it('should set the recipe public', function() {
                expect(sut.$scope.recipe.private).toBeFalsy();
            });
            it('should call publish function', function() {
                expect(sut.$scope.publish).toHaveBeenCalled();
            });
        });

        describe('savePrivate', function() {
            beforeEach(function() {
                sut.savePrivate();
            });
            it('should set the recipe private', function() {
                expect(sut.$scope.recipe.private).toBeTruthy();
            });
            it('should call publish function', function() {
                expect(sut.$scope.publish).toHaveBeenCalled();
            });
        });

    });

});