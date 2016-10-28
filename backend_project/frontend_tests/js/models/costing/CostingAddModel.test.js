/**
 * Created by apium on 23/03/2016.
 */
define(function(require) {
    var path = 'models/costing/CostingAddModel';
    describe(path, function() {
        var Model = require('models/costing/CostingAddModel');
        var PromiseHelper = require('../../../test-helpers/Promise.js');

        var sut;
        beforeEach(function() {
            sut = Model.newInstance();
            sut.$http = {};
        });

        describe('save', function() {
            it('should save costing and return promise', function() {
                var promise = {success: true};
                sut.$http.post = jasmine.createSpy().and.returnValue(PromiseHelper.fake(promise));
                var actual = sut.save();
                expect(actual.getActualResult()).toEqual(promise);
            });
        });

    });
});