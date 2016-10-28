/**
 * Created by apium on 22/03/2016.
 */
define(function (require) {
    var path = 'presenters/PaymentPresenter';
    describe(path, function () {
        var Presenter = require('presenters/PaymentPresenter');
        var PromiseHelper = require('../../test-helpers/Promise.js');

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
                    'onSubmitPayment',
                    'onSwitchPlan',
                    'onValidatePayment'
                ];
                var actual = Object.keys(exerciseShow()).sort();
                expect(actual).toEqual(events);
            });
        });

    });
});