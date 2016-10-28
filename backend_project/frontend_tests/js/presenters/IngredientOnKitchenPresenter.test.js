define(function (require) {

    var path = 'presenters/IngredientOnKitchenPresenter';
    describe(path, function () {
        var IngredientOnKitchenPresenter = require('presenters/IngredientOnKitchenPresenter');

        var sut, stubView, stubModel;

        beforeEach(function () {
            sut = IngredientOnKitchenPresenter.newInstance();
            stubView = {
                increaseIngredientInputViewTop: jasmine.createSpy()
            };
            stubModel = {
                initIngredient: jasmine.createSpy(),
                getRecipesByChefAndName: jasmine.createSpy(),
                removeIngredientAtIndex: jasmine.createSpy(),
                getRecipesByNameIndexById: jasmine.createSpy(),
                removeRecipesByNameAtIndex: jasmine.createSpy(),
                saveIngredients: jasmine.createSpy(),
                clearRecipeLink: jasmine.createSpy(),
                saveRecipeLink: jasmine.createSpy(),
                updateSubIngredients: jasmine.createSpy()
            };
        });

        describe('Ingredient', function () {
            describe('init ingredient', function() {
                var inputIngredients = [
                    {
                        name: 'name1',
                        linkRecipeId: 'linkRecipeId1'
                    },
                    {
                        name: 'name2',
                        linkRecipeId: 'linkRecipeId2'
                    }
                ];

                it('should add ingredient into model', function() {
                    sut.initIngredient(inputIngredients, stubView, stubModel);
                    expect(stubModel.initIngredient.calls.count()).toEqual(2);
                });

                it('should update view after add ingredient', function() {
                    sut.initIngredient(inputIngredients, stubView, stubModel);
                    expect(stubView.increaseIngredientInputViewTop.calls.count()).toEqual(2);
                });

                it('should get recipe for each ingredient', function() {
                    sut.initIngredient(inputIngredients, stubView, stubModel);
                    expect(stubModel.getRecipesByChefAndName.calls.count()).toEqual(2);
                });

                it('should updateSubIngredients', function () {
                    sut.initIngredient(inputIngredients, stubView, stubModel);
                    expect(stubModel.updateSubIngredients).toHaveBeenCalled();
                });
            });
            describe('remove ingredient', function() {
                var aIngredient = {
                    id: 1000
                };
                beforeEach(function() {
                    sut.removeIngredient(0, aIngredient, stubView, stubModel);
                });
                it('should remove ingredient at index on model', function() {
                   expect(stubModel.removeIngredientAtIndex).toHaveBeenCalledWith(0);
                });
                it('should get index of list recipe name by ingredient id on model', function() {
                   expect(stubModel.getRecipesByNameIndexById).toHaveBeenCalledWith(1000);
                });
                it('should remove that list recipe name on model', function() {
                   expect(stubModel.removeRecipesByNameAtIndex).toHaveBeenCalled();
                });
                it('should save ingredient on model', function() {
                   expect(stubModel.saveIngredients).toHaveBeenCalled();
                });
            });
            describe('toogleLinkToRecipe', function() {
                var aIngredient = {
                    id: 1000,
                    linkRecipeId: 1
                };
                it('should clear recipe if it is linked', function() {
                    sut.toogleLinkToRecipe(1, aIngredient, stubView, stubModel, function(){});
                    expect(stubModel.clearRecipeLink).toHaveBeenCalled();
                });
                it('should link to recipe if it is not linked', function() {
                    sut.toogleLinkToRecipe(0, aIngredient, stubView, stubModel, function(){});
                    expect(stubModel.saveRecipeLink).toHaveBeenCalled();
                });
                it('should save ingredient', function() {
                    sut.toogleLinkToRecipe(0, aIngredient, stubView, stubModel, function(){});
                    expect(stubModel.saveIngredients).toHaveBeenCalled();
                })
            });
        });

    });
});