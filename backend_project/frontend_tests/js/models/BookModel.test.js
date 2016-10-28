/**
 * Created by apium on 23/03/2016.
 */
define(function(require) {
    var path = 'models/BookModel';
    describe(path, function() {
        var Model = require('models/BookModel');
        var PromiseHelper = require('../../test-helpers/Promise.js');

        var sut;
        beforeEach(function() {
            sut = Model.newInstance();
            sut.chefModel = {};
        });

        describe('getChefByNameAndLimit', function() {
            function exerciseGetChefByNameAndLimit(response, name, page) {
                sut.chefModel.getChefByNameLimit = jasmine.createSpy().and.returnValue(PromiseHelper.fake(response));
                return sut.getChefByNameAndLimit(name, page);
            }

            describe('when call first time', function() {
                it('should return expected collaborator list', function() {
                    var name = 'name';
                    var page = 1;
                    var response = {data: {chefs: [], readmore: false}};
                    var expected = {chefs: [], readmore: false};
                    var actual = exerciseGetChefByNameAndLimit(response, name, page);
                    expect(actual.getActualResult()).toEqual(expected);
                });
            });

            describe('when call another time', function() {
                it('should increase collaborator list', function() {
                    var keyword = 'keyword';
                    sut.collaboratorList = [{}];
                    sut.collaboratorKeyword = keyword;
                    var response = {data: {chefs: [{}], readmore: false}};
                    var expected = {chefs: [{}, {}], readmore: false};
                    var actual = exerciseGetChefByNameAndLimit(response, keyword, 2);
                    expect(actual.getActualResult()).toEqual(expected);
                });
            });

            describe('when search with new keyword', function() {
                it('should clean old search', function() {
                    sut.collaboratorList = [{}];
                    sut.collaboratorKeyword = 'keyword';
                    var response = {data: {chefs: [{}, {}, {}], readmore: false}};
                    var expected = {chefs: [{}, {}, {}], readmore: false};
                    var actual = exerciseGetChefByNameAndLimit(response, 'another keyword', 1);
                    expect(actual.getActualResult()).toEqual(expected);
                });
            });
        });

    });
});