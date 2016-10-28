/**
 * Created by apium on 23/03/2016.
 */
define(function(require) {
    var path = 'models/costing/CostingModel';
    describe(path, function() {
        var Model = require('models/costing/CostingModel');
        var PromiseHelper = require('../../../test-helpers/Promise.js');

        var sut;
        beforeEach(function() {
            sut = Model.newInstance();
            sut.$http = {};
            sut.$q = {};
        });

        describe('getCostingTable', function() {
            it('should set costing table', function() {
                var expected = [{}];
                sut.$http.get = jasmine.createSpy().and.returnValue(PromiseHelper.fake({data: expected}));
                sut.getCostingTable();
                expect(sut.costingTable).toEqual(expected);
            });
        });

        describe('delete', function() {
            var actual;
            beforeEach(function() {
                var response = PromiseHelper.exerciseFakeOk();
                var args = {id: 1, genericIngredientId: 2};
                sut.$http.delete = jasmine.createSpy().and.returnValue(response);
                sut.$http.put = jasmine.createSpy().and.returnValue(response);
                sut.$q.all = jasmine.createSpy().and.returnValue(response);
                actual = sut.delete(args);
            });

            it('should send delete request to backend', function() {
                expect(sut.$http.delete).toHaveBeenCalledWith('/0/custom-ingredient?id=1');
            });

            it('should send put request to backend', function() {
                expect(sut.$http.delete).toHaveBeenCalledWith('/0/costing-generic-ingredient?id=2');
            });

            it('should return promise', function() {
                expect(actual).toEqual(PromiseHelper.exerciseFakeOk());
            });
        });

        describe('duplicate', function() {
            describe('when costing have custom id', function() {
                it('should call post method', function() {
                    var costing = {custom_id: 1};
                    var spy = sut.$http.post = jasmine.createSpy().and.returnValue(PromiseHelper.exerciseFakeOk());
                    spyOn(sut, 'getCostingTable');
                    sut.duplicate(costing);
                    expect(spy).toHaveBeenCalled();
                    expect(sut.getCostingTable).toHaveBeenCalled();
                });
            });

            describe('when costing is generic item', function() {
                it('should call put method', function() {
                    var costing = {custom_id: null};
                    var spy = sut.$http.put = jasmine.createSpy().and.returnValue(PromiseHelper.exerciseFakeOk());
                    spyOn(sut, 'getCostingTable');
                    sut.duplicate(costing);
                    expect(spy).toHaveBeenCalled();
                    expect(sut.getCostingTable).toHaveBeenCalled();
                });
            });
        });

    });
});