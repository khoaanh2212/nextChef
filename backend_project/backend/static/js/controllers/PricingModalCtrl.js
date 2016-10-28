/**
 * Created by apium on 29/03/2016.
 */
;(function (app, window) {
    'use strict';

    var deps = ['$scope'];

    app.controller("PricingModalController", deps.concat([function ($scope) {
        PricingModalController.$scope = $scope;
        return PricingModalController.newInstance();
    }]));

    if (window.define) define(function () {
        return PricingModalController;
    });

    function PricingModalController($scope) {
        this.$scope = $scope;
        this.USER_TYPE = USER_TYPE;
        this.$scope.onLoad = this.init.bind(this);
        this.$scope.onClickUpgrade = this.publishEventUpgrade.bind(this);
    }

    PricingModalController.newInstance = function ($scope) {
        return new PricingModalController($scope || PricingModalController.$scope);
    };

    PricingModalController.prototype.init = function () {
        this.openModal();
    };

    PricingModalController.prototype.openModal = function() {
        if (this.USER_TYPE === 'default' || this.USER_TYPE === 'pro') {
            $('#pricing-modal').modal('show');
        }
    };

    PricingModalController.prototype.showError = function (error) {
        console.log(error);
    };

    PricingModalController.prototype.publishEventUpgrade = function() {
        this.$scope.$emit('onUpgradeBusinessPricingModal', {level: 'business', onUpgrade: true});
    };

})(app, this);