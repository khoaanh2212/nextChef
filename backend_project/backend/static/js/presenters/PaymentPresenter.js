/**
 * Created by Kate on 3/22/16.
 */
;(function (app, window) {
    'use strict';

    var deps = ['PresenterHandlerCreator'];

    function Factory(PresenterHandlerCreator) {
        PaymentPresenter.PresenterHandlerCreator = PresenterHandlerCreator;
        return PaymentPresenter;
    }

    Factory.$inject = deps;

    app.factory('PaymentPresenter', Factory);
    if (window.define) define(Factory);

    function PaymentPresenter(PresenterHandlerCreator) {
        this.Creator = PresenterHandlerCreator;
    }

    PaymentPresenter.prototype.show = function(view, model) {
        var creator = this.Creator.newInstance(this, view, model);
        return {
            onLoad: creator.createEventHandler({
                modelMethod: 'onLoad',
                viewSuccess: 'onLoaded'
            }),
            onSwitchPlan: creator.createEventHandler({
                modelMethod: 'switchPlan',
                viewSuccess: 'onPlanSwitched'
            }),
            onValidatePayment: creator.createEventHandler({
                modelMethod: 'onValidatePayment',
                viewSuccess: 'onPaymentValidated'
            }),
            onSubmitPayment: creator.createEventHandler({
                modelMethod: 'onSubmitPayment',
                viewSuccess: 'onSubmitPayment'
            })
        };
    };

    PaymentPresenter.newInstance = function(PresenterHandlerCreator) {
        return new PaymentPresenter(PresenterHandlerCreator || PaymentPresenter.PresenterHandlerCreator);
    }

})(app, this);