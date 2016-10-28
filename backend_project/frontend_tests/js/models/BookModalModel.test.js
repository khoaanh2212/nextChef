/**
 * Created by apium on 24/03/2016.
 */
define(function(require) {
    var path = 'models/BookModalModel';
    describe(path, function() {
        var Model = require('models/BookModalModel');
        var PromiseHelper = require('../../test-helpers/Promise.js');

        var sut;
        beforeEach(function() {
            sut = Model.newInstance({}, {});
            sut.bookObject = {};
        });

        describe('createBook', function() {
            it('should call to adding book with data', function() {
                var actual = sut.bookObject.addBook = jasmine.createSpy().and.returnValue(PromiseHelper.exerciseFakeOk());
                var input = {
                    name: 'name',
                    private: 0,
                    collaborators: [ {id: '1'}, {id: '2'} ]
                };

                var expected = {
                    name: 'name',
                    private: 0,
                    collaborators: '1,2'
                };

                sut.createBook(input);
                expect(actual).toHaveBeenCalledWith(expected);
            });
        });

    });
});