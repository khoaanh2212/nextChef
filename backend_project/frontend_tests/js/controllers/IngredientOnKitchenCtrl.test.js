define(function (require) {

    var path = 'controllers/IngredientOnKitchenCtrl';
    describe(path, function () {
        var IngredientOnKitchenController = require('controllers/IngredientOnKitchenCtrl');

        var sut, stubPresenter, stubModel;

        beforeEach(function () {
            stubPresenter = {
                initIngredient: jasmine.createSpy(),
                removeIngredient: jasmine.createSpy(),
                toogleLinkToRecipe: jasmine.createSpy()
            };
            stubModel = {
            };
            sut = IngredientOnKitchenController.newInstance(stubModel, stubPresenter);
        });

        describe('Ingredient', function () {
            describe('init ingredient', function() {
                it('should call init ingredient function of presenter', function() {
                    sut.initIngredient({});
                    expect(stubPresenter.initIngredient).toHaveBeenCalled();
                });
            });
            describe('fill ingredients suggestion data', function() {
                var suggestionIngredient = [
                    {
                        id: 1,
                        name: 'test1'
                    },
                    {
                        id: 2,
                        name: 'test2'
                    }
                ];
                it('should just get name', function() {
                    var expected = ['test1','test2'];
                    sut.fillIngredientsSuggestionData(suggestionIngredient);
                    expect(sut.ingredientsSuggestion).toEqual(expected);
                });
                it('should show ingredient suggestion popup after fill data', function() {
                    sut.fillIngredientsSuggestionData(suggestionIngredient);
                    expect(sut.showIngredientSuggestionResult).toEqual(true);
                });
            });
            describe('remove ingredient', function() {
               it('should call remove ingredient function of presenter', function() {
                  sut.removeIngredient(0,{});
                  expect(stubPresenter.removeIngredient).toHaveBeenCalled();
               });
            });
            describe('link recipe', function() {
               it('should call link recipe function of presenter', function() {
                  sut.toogleLinkToRecipe(0, {}, function(){});
                  expect(stubPresenter.toogleLinkToRecipe).toHaveBeenCalled();
               });
            });
        });

    });
});
