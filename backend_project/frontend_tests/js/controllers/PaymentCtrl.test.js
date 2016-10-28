/**
 * Created by Kate on 3/22/16.
 */
define(function (require) {

    describe('PaymentController', function () {

        var PaymentController = require('controllers/PaymentCtrl');

        var sut;

        beforeEach(function () {
            $scope = {};
            model = {};
            presenter = {show: function() {}};
            localStorage = {};
            sut = PaymentController.newInstance($scope, model, presenter, localStorage);
            sut.$scope.events = {};
        });

        describe('fn', function () {
            var expected = ['init', 'switchType', 'switchInterval', 'submitPayment'];
            describe('always', function () {
                it('should define expected properties in fn', function () {
                    var actual = Object.keys(sut.$scope.fn);
                    expect(actual).toEqual(expected);
                });

                it('should define only functions', function () {
                    var fn = sut.$scope.fn;
                    Object.keys(fn).forEach(function (key) {
                        expect(typeof fn[key]).toBe('function');
                    });
                });
            });
        });

        describe('onLoaded', function () {
            it('should apply the response to view', function () {
                response = {
                    plan: 'plan', months: 'months', years: 'years'
                };
                sut.onLoaded(response);
                expect(sut.$scope.plan).toEqual('plan');
                expect(sut.$scope.months).toEqual('months');
                expect(sut.$scope.years).toEqual('years');
            })
        });

        describe('switchType', function() {
            it('should call to event switchPlan with "type"', function() {
                sut.$scope.events.onSwitchPlan = jasmine.createSpy();
                sut.switchType();
                expect(sut.$scope.events.onSwitchPlan).toHaveBeenCalledWith('type');
            });
        });

        describe('switchInterval', function() {
            it('should call to event switchPlan with "interval"', function() {
                sut.$scope.events.onSwitchPlan = jasmine.createSpy();
                sut.switchInterval();
                expect(sut.$scope.events.onSwitchPlan).toHaveBeenCalledWith('interval');
            });
        });

    });

});