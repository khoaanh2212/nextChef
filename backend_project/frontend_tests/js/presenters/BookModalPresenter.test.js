/**
 * Created by apium on 24/03/2016.
 */
define(function (require) {
    var path = 'presenters/BookModalPresenter';
    describe(path, function () {
        var Presenter = require('presenters/BookModalPresenter');

        var view, model, sut;
        beforeEach(function () {
            creator = {
                newInstance: function() {
                    return {
                        createEventHandler: function() {}
                    };
                }
            };
            sut = Presenter.newInstance(creator);
            view = {};
            model = {};
        });

        function exerciseShow() {
            return sut.show(view, model);
        }

        describe('show', function () {
            it('should define events', function () {
                var events = [
                    'onLoad',
                    'onClickAddingBook',
                    'onChangeGetCollaborator',
                    'onLoadCollarboratorBeforeEdit',
                    'clearCollaboratorsList'
                ];
                var actual = Object.keys(exerciseShow());
                expect(actual).toEqual(events);
            });
        });

    });
});