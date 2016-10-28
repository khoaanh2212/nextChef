/**
 * Created by apium on 22/03/2016.
 */
define(function(require) {
    var path = 'presenters/BookPresenter';
    describe(path, function() {
        var Presenter = require('presenters/BookPresenter');
        var PromiseHelper = require('../../test-helpers/Promise.js');

        var view, model, sut;
        beforeEach(function() {
            sut = Presenter.newInstance();
            view = {};
            model = {};
        });

        function exerciseShow() {
            return sut.show(view, model);
        }

        describe('show', function() {
            it('should define events', function() {
                var events = ['onChangeGetCollaborator'];
                var actual =  Object.keys(exerciseShow()).sort();
                expect(actual).toEqual(events);
            });
        });

        describe('handleOnChangeGetCollaborator', function() {
            function exerciseHandleOnChage(response, keyword, page) {
                keyword = keyword || 'some keyword';
                page = page || 1;
                view.showError = jasmine.createSpy();
                view.initCollaboratorDropdown = jasmine.createSpy();
                model.getChefByNameAndLimit = jasmine.createSpy().and.returnValue(response);
                return sut.handleOnChangeGetCollaborator(view, model, keyword, page);
            }

            it('should call the model', function() {
                var keyword = 'this is keyword';
                var page = 'paging';
                exerciseHandleOnChage(PromiseHelper.exerciseFakeOk(), keyword, page);
                expect(model.getChefByNameAndLimit).toHaveBeenCalledWith(keyword, page);
            });

            it('should call to view', function() {
                var expected = PromiseHelper.fake({data: {}});
                exerciseHandleOnChage(expected);
                expect(view.initCollaboratorDropdown).toHaveBeenCalled();
            });

            it('should show an error', function() {
                var response = PromiseHelper.exerciseFakeFail();
                exerciseHandleOnChage(response);
                expect(view.showError).toHaveBeenCalled();
            });
        });
    });
});