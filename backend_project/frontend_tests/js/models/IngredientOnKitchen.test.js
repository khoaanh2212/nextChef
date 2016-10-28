define(function (require) {

    var path = 'models/IngredientOnKitchenModel';
    describe(path, function () {
        var IngredientOnKitchenModel = require('models/IngredientOnKitchenModel');
        var PromiseHelper = require('../../test-helpers/Promise.js');

        var sut, stubRecipe, stubChef;

        beforeEach(function () {
            var ajaxService = {};
            sut = IngredientOnKitchenModel.newInstance(ajaxService);
            stubRecipe = sut.recipe = {};
            stubChef = sut.chef = {};
        });

        describe('Ingredient', function () {
            describe('init ingredient', function () {
                var inputIngredient = {
                        name: 'name1',
                        linkRecipeId: 'linkRecipeId1'
                    };

                it('should init with id', function () {
                    var expected = [
                        {
                            id: 'ingredients0',
                            name: 'name1',
                            linkRecipeId: 'linkRecipeId1'
                        }
                    ];
                    sut.initIngredient(inputIngredient, 0);

                    expect(sut.ingredients).toEqual(expected);
                });

            });

            describe('modify ingredient', function () {
                beforeEach(function () {
                    sut.ingredients = [
                        {
                            id: 'ingredients0',
                            name: 'name1',
                            linkRecipeId: 'linkRecipeId1'
                        },
                        {
                            id: 'ingredients1',
                            name: 'name2',
                            linkRecipeId: 'linkRecipeId2'
                        }
                    ];
                });
                describe('addSelectedIngredient', function () {
                    it('should add new ingredient width id equal current length of ingredient array', function () {
                        var expected = [
                            {
                                id: 'ingredients0',
                                name: 'name1',
                                linkRecipeId: 'linkRecipeId1'
                            },
                            {
                                id: 'ingredients1',
                                name: 'name2',
                                linkRecipeId: 'linkRecipeId2'
                            },
                            {
                                id: 'ingredients2',
                                name: 'name3',
                                linkRecipeId: null
                            }
                        ];
                        sut.addSelectedIngredient('name3');
                        expect(sut.ingredients).toEqual(expected);
                    });
                });
                describe('updateSubIngredients', function () {

                    it('should update ingredients list with sub ingredient when needed', function () {

                        sut.ajaxService.ok = jasmine.createSpy().and.returnValue(PromiseHelper.fake({ingredients: []}));

                        sut.ingredients = [
                            {
                                name: 'ingr1', linkRecipeId: '1'
                            },
                            {
                                name: 'ingr2', linkRecipeId: '2'
                            },
                            {
                                name: 'ingr3', linkRecipeId: null, subIngredients: []
                            }
                        ];

                        var expected = [
                            {
                                name: 'ingr1', linkRecipeId: '1', subIngredients: []
                            },
                            {
                                name: 'ingr2', linkRecipeId: '2', subIngredients: []
                            },
                            {
                                name: 'ingr3', linkRecipeId: null
                            }
                        ];

                        sut.updateSubIngredients();
                        expect(sut.ingredients).toEqual(expected);
                   });
               });
              describe('_getSubIngredients', function () {
                    beforeEach(function () {
                        sut.ajaxService.ok = jasmine.createSpy().and.returnValue(PromiseHelper.fake({ingredients: []}));
                        sut._getSubIngredients({ linkRecipeId: 1 });
                    });

                    it('should call once to the ajax service', function () {
                        expect(sut.ajaxService.ok.calls.count()).toBe(1)
                    });

                    it('should call the ajax service with parameters', function () {
                        var expected_url  = '/0/recipes/1/ingredients';
                        expect(sut.ajaxService.ok.calls.allArgs()).toEqual([
                            ['GET', expected_url]
                        ]);
                    });
              });
               describe('removeIngredient', function() {
                   it('should remove ingredient in ingredient array at index', function() {
                      var expected = [
                        {
                           id: 'ingredients0',
                           name: 'name1',
                           linkRecipeId: 'linkRecipeId1'
                        }
                      ];
                      sut.removeIngredientAtIndex(1);
                      expect(sut.ingredients).toEqual(expected);
                   });
               });
            });
            describe('recipe', function() {
                beforeEach(function() {
                   sut.ingredients = [
                        {
                           id: 'ingredients0',
                           name: 'name1',
                           linkRecipeId: null
                        },
                        {
                           id: 'ingredients1',
                           name: 'name2',
                           linkRecipeId: 'linkRecipeId2'
                        }
                   ];
                });
                describe('clearRecipeLink', function () {
                    it('should call to updateSubIngredients', function () {
                        sut.ingredients = [];
                        sut.updateSubIngredients = jasmine.createSpy();
                        sut.clearRecipeLink();
                        expect(sut.updateSubIngredients).toHaveBeenCalled();
                    });
                });

                describe('saveRecipeLink', function () {
                    it('should call to updateSubIngredients', function () {
                        sut.ingredients = [];
                        sut.updateSubIngredients = jasmine.createSpy();
                        sut.saveRecipeLink();
                        expect(sut.updateSubIngredients).toHaveBeenCalled();
                    });
                });
            });
        });
    });
});