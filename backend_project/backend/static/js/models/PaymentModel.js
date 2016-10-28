/**
 * Created by Kate on 3/22/16.
 */
;(function (app, window) {
    'use strict';

    var deps = ['Plan', 'Stripe', 'AjaxService', '$q'];

    app.factory('PaymentModel', Factory);

    function Factory(Plan, Stripe, AjaxService, $q) {
        PaymentModel.Plan = Plan;
        PaymentModel.Stripe = Stripe;
        PaymentModel.AjaxService = AjaxService;
        PaymentModel.$q = $q;
        return PaymentModel;
    }

    Factory.$inject = deps;

    if (window.define) define(Factory);

    function PaymentModel(plan, stripe, ajaxService, Q) {
        this.plan = plan;
        this.stripe = stripe;
        this.ajaxService = ajaxService;
        this.Q = Q;
    }

    PaymentModel.prototype.onLoad = function () {
        var months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
        var years = this._getYears();
        return this.Q.all({
            plan: this.plan,
            months: months,
            years: years

        });
    };

    PaymentModel.prototype.switchPlan = function (criteria) {
        criteria == 'type' ? this.plan.switchType() : this.plan.switchInterval();
        var url = GET_PLAN_URL + '?type=' + this.plan.type + '&interval=' + this.plan.interval;
        var self = this;
        return this.ajaxService.ok('GET', url).then(function (response) {
            self.plan.amount = response.amount;
            self.plan.dueDate = response.due_date;
            return self.plan;
        });
    };

    PaymentModel.prototype.onValidatePayment = function (cardInfo) {

        this.stripe.setCardNumber(cardInfo.cardNumber);
        this.stripe.setCardCVC(cardInfo.cardCVC);
        this.stripe.setCardExpiryMonth(cardInfo.cardExpiryMonth);
        this.stripe.setCardExpiryYear(cardInfo.cardExpiryYear);
        return this.Q.all({
            isValidated: this.stripe.validate(),
            errors: this.stripe.errors
        });

    };

    PaymentModel.prototype.onSubmitPayment = function () {
        var deferred = this.Q.defer();
        this.stripe.createToken(function (status, response) {
            deferred.resolve(response);
        });
        return deferred.promise;
    };

    PaymentModel.prototype._getYears = function () {
        var result = [];
        var currentYear = (new Date()).getFullYear();
        for (var y = 0; y < 20; y++) {
            result.push(currentYear + y);
        }
        return result;
    };

    PaymentModel.newInstance = function (plan, stripe, ajaxService, Q) {
        plan = plan || PaymentModel.Plan.newInstance(PLAN_TYPE, PLAN_INTERVAL, AMOUNT, DUE_DATE);
        stripe = stripe || PaymentModel.Stripe.newInstance();
        ajaxService = ajaxService || PaymentModel.AjaxService.newInstance();
        Q = Q || PaymentModel.$q;
        return new PaymentModel(plan, stripe, ajaxService, Q);
    }

})(app, this);