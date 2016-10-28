;(function (app, window) {
    'use strict';

    var deps = ['$scope', 'PaymentModel', 'PaymentPresenter', 'infrastructure/LocalStorage'];

    app.controller("PaymentController", deps.concat([function($scope, PaymentModel, PaymentPresenter, localStorage) {
        PaymentController.$scope = $scope;
        PaymentController.PaymentModel = PaymentModel;
        PaymentController.PaymentPresenter = PaymentPresenter;
        PaymentController.localStorage = localStorage;
        return PaymentController.newInstance();
    }]));

    if (window.define) define(function() {
        return PaymentController;
    });

    function PaymentController($scope, model, presenter, localStorage) {
        this.$scope = $scope;
        this.localStorage = localStorage;
        this.$scope.events = presenter.show(this, model);
        this._initFn();
    }

    PaymentController.prototype._initFn = function() {
        this.$scope.fn = {
            init: this.onLoad.bind(this),
            switchType: this.switchType.bind(this),
            switchInterval: this.switchInterval.bind(this),
            submitPayment: this.beforeSubmitPayment.bind(this)
        };
    };

    PaymentController.prototype.onLoad = function() {
        this.$scope.events.onLoad();
    };

    PaymentController.prototype.switchType = function() {
        this.$scope.events.onSwitchPlan('type');
    };

    PaymentController.prototype.switchInterval = function() {
        this.$scope.events.onSwitchPlan('interval');
    };

    PaymentController.prototype.onLoaded = function (response) {
        this.$scope.plan = response.plan;
        this.$scope.months = response.months;
        this.$scope.years = response.years;
    };

    PaymentController.prototype.onPlanSwitched = function (plan) {
        this.$scope.plan = plan;
    };

    PaymentController.prototype.beforeSubmitPayment = function() {
        var cardInfo = {
            cardNumber: this.$scope.cardNumber,
            cardCVC: this.$scope.cardCVC,
            cardExpiryMonth: this.$scope.cardExpiryMonth,
            cardExpiryYear: this.$scope.cardExpiryYear
        };
        this.$scope.events.onValidatePayment(cardInfo);
    };

    PaymentController.prototype.onPaymentValidated = function(response) {
        if(response.isValidated) {
            this.$scope.events.onSubmitPayment();
        } else if (response.errors) {
            this.$scope.errors = response.errors;
        }
    };

    PaymentController.prototype.onSubmitPayment = function(response) {
        $('#token').val(response.id);
        $('#last4').val(response.card.last4);
        this.setUpgradeFromCostingPage();
        document.getElementById('billing-submission').submit();
    };

    PaymentController.prototype.showError = function(error) {
        console.log(error);
    };

    PaymentController.newInstance = function ($scope, model, presenter, localStorage) {
        $scope = $scope || PaymentController.$scope;
        model = model || PaymentController.PaymentModel.newInstance();
        presenter = presenter || PaymentController.PaymentPresenter.newInstance();
        localStorage = localStorage || PaymentController.localStorage.newInstance();

        var instance = new PaymentController(
            $scope, model, presenter, localStorage
        );
        //var aspect = ApplyAspect.newInstance();
        //aspect.weave(instance);
        return instance;
    };

    PaymentController.prototype.setUpgradeFromCostingPage = function() {
        var costingPage = this.localStorage.get('costing_upgrade');
        if (costingPage) {
            $('#costingPage').val(costingPage);
        }
    };

})(app, this);
