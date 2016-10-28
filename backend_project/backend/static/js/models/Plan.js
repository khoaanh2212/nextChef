;(function (app, window) {
    'use strict';
    app.factory('Plan', ['$http', function ($http) {
        window.$http = $http;
        return Plan;
    }]);

    if (window.define) define(function (require) {
        return Plan;
    });

    var PLAN_PRO = 'pro';
    var PLAN_BUSINESS = 'business';
    var PLAN_MONTHLY = 'monthly';
    var PLAN_ANNUALLY = 'annually';

    function Plan(type, interval, amount, dueDate) {
        this.type = type;
        this.interval = interval;
        this.amount = amount;
        this.dueDate = dueDate;

        this.nextType = this.getNextType();
        this.nextInterval = this.getNextInterval();

        this.RestAPI = window.RestAPI;
    }

    Plan.prototype.getNextType = function () {
        return this.type == PLAN_PRO ? PLAN_BUSINESS : PLAN_PRO;
    };

    Plan.prototype.getNextInterval = function () {
        return this.interval == PLAN_MONTHLY ? PLAN_ANNUALLY : PLAN_MONTHLY;
    };

    Plan.prototype.switchType = function () {
        this.nextType = this.type;
        this.type = this.getNextType();
    };

    Plan.prototype.switchInterval = function () {
        this.nextInterval = this.interval;
        this.interval = this.getNextInterval();
    };

    Plan.newInstance = function (type, interval, amount, dueDate) {
        return new Plan(type, interval, amount, dueDate);
    };

})(app, this);
