/**
 * Created by apium on 05/04/2016.
 */
define(function (require) {
    var path = 'models/kitchen/IngredientModel';
    describe(path, function () {
        var Model = require('models/kitchen/IngredientModel');
        var PromiseHelper = require('../../../test-helpers/Promise.js');

        var sut;
        beforeEach(function () {
            sut = Model.newInstance();
            sut.$http = {};
            sut.$q = {};
        });

        describe('makeDropdownList', function () {
            var actual;
            beforeEach(function () {
                var response = PromiseHelper.exerciseFakeOk();
                sut.$http.get = jasmine.createSpy().and.returnValue(response);
                sut.$q.all = jasmine.createSpy().and.returnValue(response);
                spyOn(sut, 'setIngredients');
                spyOn(sut, 'setRecipes');
                actual = sut.makeDropdownList('ingredient str');
            });

            it('should call to get ingredient and recipes', function () {
                expect(sut.$http.get.calls.count()).toBe(2);
            });

            it('should call method $q to get multi request', function () {
                expect(sut.$q.all).toHaveBeenCalled();
            });

            it('should return expected', function () {
                var expected = {
                    ingredients: [],
                    isShowMoreIngredient: true,
                    recipes: [],
                    isShowMoreRecipe: true,
                    isShow: true
                };
                expect(actual.getActualResult()).toEqual(expected);
            });
        });

        describe('makeSelectedIngredient', function () {
            it('should set ingredient', function () {
                var ingredient = {};
                sut.makeSelectedIngredient(ingredient);
                expect(sut.selectedIngredient).toEqual(ingredient);
            });

            it('should return expected', function () {
                var actual = sut.makeSelectedIngredient('expected');
                expect(actual).toEqual('expected');
            });
        });

        describe('getMoreIngredient', function () {
            it('should get more ingredient and add to old list', function () {
                sut.ingredients.list = [{}];
                sut.$http.get = jasmine.createSpy().and.returnValue(PromiseHelper.fake({data: {list: [{}, {}]}}));
                sut.getMoreIngredient();
                expect(sut.ingredients.list.length).toBe(3);
            });
        });

        describe('getMoreRecipe', function () {
            it('should get more recipe and add to old list', function () {
                sut.recipes.list = [{}];
                sut.$http.get = jasmine.createSpy().and.returnValue(PromiseHelper.fake({data: {list: [{}, {}]}}));
                sut.getMoreRecipe();
                expect(sut.recipes.list.length).toBe(3);
            });
        });

        describe('validateAdding', function () {
            describe('when adding ingredient', function () {
                it('should send request with expected data', function () {
                    window.RECIPE_ID = 1;
                    sut.selectedIngredient = {custom_id: 1};
                    var expected = {
                        costing_ingredient_id: 1,
                        is_custom: true,
                        text: 1
                    };
                    var spy = sut.$http.post = jasmine.createSpy().and.returnValue(PromiseHelper.exerciseFakeOk());
                    sut.validateAdding({amount: 1});
                    expect(spy).toHaveBeenCalledWith('/0/recipes/1/ingredient', expected);
                });
            });

            describe('when adding recipe', function () {
                it('should send request with expected', function () {
                    window.RECIPE_ID = 1;
                    sut.selectedIngredient = {id: 1};
                    var expected = {
                        recipe_id: 1,
                        subrecipe_id: 1,
                        amount: 1
                    };
                    var spy = sut.$http.post = jasmine.createSpy().and.returnValue(PromiseHelper.exerciseFakeOk());
                    sut.validateAdding({amount: 1});
                    expect(spy).toHaveBeenCalledWith('/0/subrecipes', expected);
                });
            });
        });

        describe('handleIngredient', function () {
            // describe('when context.amount empty', function () {
            //     it('should return false', function () {
            //         var context = {amount: null, ingredient: 'ingredient'}
            //         expect(sut.handleIngredient(context)).toEqual(false);
            //     });
            // });
            describe('when context.amount not empty', function () {
                describe('when ingredient is already exists,running adding ingredient into recipe', function () {
                    it('should send request with expected data', function () {
                        window.RECIPE_ID = 1;
                        sut.selectedIngredient = {custom_id: 1};
                        var expected = {
                            costing_ingredient_id: 1,
                            is_custom: true,
                            text: 1
                        }
                        var spy = sut.$http.post = jasmine.createSpy().and.returnValue(PromiseHelper.exerciseFakeOk());
                        sut.checkIngredientsIsAlreadyExists = jasmine.createSpy().and.returnValue(1);
                        sut.handleIngredient({amount: 1, ingredient: 'ingredients'});
                        expect(spy).toHaveBeenCalledWith('/0/recipes/1/ingredient', expected);

                    });
                });
                describe('when ingredient is already not exists', function () {
                    it('should call to function handle with new ingredient', function () {
                        var context = {amount: 1, ingredient: 'ingredients'};
                        var spy = sut.handleWithNewIngredient = jasmine.createSpy().and.returnValue(PromiseHelper.exerciseFakeOk());
                        sut.checkIngredientsIsAlreadyExists = jasmine.createSpy().and.returnValue(false);
                        sut.handleIngredient(context);
                        expect(spy).toHaveBeenCalledWith(context);
                    });
                });
            });
        });
        describe('handleWithNewIngredient', function () {
            describe('when context of ingredient is not valid', function () {
                it('should return object with message error', function () {
                    sut.isValidatingIngredient = jasmine.createSpy().and.returnValue(false);
                    var expected = {invalid: true, msg: 'amount is required'}
                    expect(sut.handleWithNewIngredient({})).toEqual(expected);
                });
            });
            describe('when context of ingredient is valid', function () {
                it('should send request with expected data', function () {
                    window.RECIPE_ID = 1;
                    sut.selectedIngredient = {custom_id: 1};
                    var expected = {
                        costing_ingredient_id: 'New ingredient',
                        is_custom: true,
                        text: '1'
                    }
                    var spy = sut.$http.post = jasmine.createSpy().and.returnValue(PromiseHelper.exerciseFakeOk());
                    sut.handleWithNewIngredient({amount: '1', ingredient: 'new ingredient'});
                    expect(spy).toHaveBeenCalledWith('/0/recipes/1/ingredient', expected);

                });
            });
        });
        describe('getIngredientList', function () {
            it('should get ingredient list', function () {
                var response = {data: {ingredients: [], allergens: []}};
                var spy = sut.$http.get = jasmine.createSpy().and.returnValue(PromiseHelper.fake(response));
                var actual = sut.getIngredientList();
                expect(spy).toHaveBeenCalled();
                expect(actual.getActualResult()).toEqual({ingredientList: [], allergens: [], message: ''});
            });

            it('should return expected data', function () {
                var response = {
                    data: {
                        ingredients: [
                            {
                                id: 1,
                                text: '1 large apple',
                                quantity: 1,
                                type: 'ingredient',
                                measure: 'large',
                                name: 'apple'
                            },
                            {id: 2, name: 'recipe', owner_name: 'chef', type: 'recipe', subrecipe_id: 1, amount: 'one'}
                        ],
                        allergens: []
                    }
                };
                var expected = {
                    ingredientList: [
                        {id: 1, name: '1 large apple'},
                        {id: 2, name: 'one recipe', chef_name: 'chef', link: '/recipe/recipe-1'}
                    ],
                    allergens: [],
                    message: ''
                };
                sut.$http.get = jasmine.createSpy().and.returnValue(PromiseHelper.fake(response));
                var actual = sut.getIngredientList();
                expect(actual.getActualResult()).toEqual(expected);
            });
        });

        describe('clearSelectedIngredient', function () {
            it('should return selected ingredient to false', function () {
                sut.selectedIngredient = {}
                sut.clearSelectedIngredient();
                expect(sut.selectedIngredient).toEqual(false);
            });
        });

        describe('checkIngredientsIsAlreadyExists', function () {
            describe('when ingredient list is empty', function () {
                it('should return false', function () {
                    sut.ingredients.list = [];
                    var ingredient = 'ingredients';
                    expect(sut.checkIngredientsIsAlreadyExists(ingredient)).toEqual(false);
                })
            });
            describe('when ingredient list not empty', function () {
                it('should return false if ingredient not in ingredient list', function () {
                    sut.ingredients.list = [{ingredient: 'something', generic_table_row_id: 1}];
                    var ingredient = 'ingredients';
                    expect(sut.checkIngredientsIsAlreadyExists(ingredient)).toEqual(false);
                });
                it('should return false if ingredient in ingredient list', function () {
                    sut.ingredients.list = [{
                        ingredient: 'something',
                        generic_table_row_id: 1
                    }, {ingredient: 'ingredients', generic_table_row_id: 2}];
                    var ingredient = 'ingredients';
                    expect(sut.checkIngredientsIsAlreadyExists(ingredient)).toEqual(2);
                });
            });
        });

        describe('checkSubRecipeIsAlreadyExists', function () {
            describe('when list sub recipe is null', function () {
                it('should return true', function () {
                    actual = sut.checkSubRecipeIsAlreadyExists('subRecipe');
                    expect(actual).toEqual(false);
                });
            });
            describe('when list sub recipe has length is 0', function () {
                it('should return true', function () {
                    sut.recipes.list = [];
                    actual = sut.checkSubRecipeIsAlreadyExists('subRecipe');
                    expect(actual).toEqual(false);
                });
            });
            describe('when list sub not empty and subrecipe not in sub recipe list', function () {
                it('should return false', function () {
                    sut.recipes.list = [{id: 1, name: 'sub recipe 1'}, {id: 2, name: ' sub recipes 2'}]
                    actual = sut.checkSubRecipeIsAlreadyExists('subrecipe');
                    expect(actual).toEqual(false);
                });
            });
            describe('when list sub recipe not empty and subrecipe in sub recipe list', function () {
                it('should return id of sub recipe', function () {
                    sut.recipes.list = [{id: 1, name: 'sub recipe 1'}, {id: 2, name: 'subrecipe'}]
                    actual = sut.checkSubRecipeIsAlreadyExists('subrecipe');
                    expect(actual).toEqual(2);
                });
            });

        });

        describe('isValidatingIngredient', function () {
            describe('when ingredient is wrong', function () {
                it('should return false', function () {
                    var context = {amount: '', ingredient: 'ingredients'}
                    var actual = sut.isValidatingIngredient(context);
                    expect(actual).toEqual(false);
                });
            });
            describe('when ingredient is right', function () {
                it('should return true', function () {
                    var context = {amount: '1', ingredient: 'ingredients'}
                    var actual = sut.isValidatingIngredient(context);
                    expect(actual).toEqual(true);
                });
            });
        });

    });
});