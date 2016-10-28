define(function (require) {
    var path = 'presenters/AllergenPresenter';
    describe(path, function () {
        var Presenter = require('presenters/AllergenPresenter');

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
                var events = ['onUpdateAllergen'];
                var actual = Object.keys(exerciseShow()).sort();
                expect(actual).toEqual(events);
            });
        });

    });
});