define(function (require) {
    describe('models/PaymentModel', function () {

        var PaymentModel = require('models/PaymentModel');
        var PromiseHelper = require('../../test-helpers/Promise.js');

        var sut, plan, stripe;

        beforeEach(function () {
            plan = {}, stripe = {}, ajaxService = {}, Q = {};
            sut = PaymentModel.newInstance(plan, stripe, ajaxService, Q);
        });

        function fake(expected) {
            return PromiseHelper.fake(expected);
        }

        describe('onLoad', function () {
            var actual, expected = {
                plan: {},
                months: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                years: 'years'
            };

            it('should return expected data', function () {
                sut.Q.all = jasmine.createSpy().and.returnValue(PromiseHelper.fake(expected));
                sut._getYears = jasmine.createSpy().and.returnValue('years');
                actual = sut.onLoad().getActualResult();
                expect(sut.Q.all).toHaveBeenCalledWith(expected);
                expect(actual).toEqual(expected);
            });

        });

        describe('switchPlan', function () {

            var spy = jasmine.createSpy();

            beforeEach(function () {
                window.GET_PLAN_URL = 'plan_url';
                sut.ajaxService.ok = jasmine.createSpy().and.returnValue(PromiseHelper.fake({
                    amount: 5.0,
                    due_date: '2015-01-01'
                }));
                sut.plan = {
                    type: 'pro', interval: 'annually', switchType: spy, switchInterval: spy
                };
            });

            it('should call to switchType function if criteria is "type"', function () {
                sut.switchPlan('type');
                expect(sut.plan.switchType).toHaveBeenCalled();
            });

            it('should call to switchInterval function if criteria is "interval"', function () {
                sut.switchPlan('interval');
                expect(sut.plan.switchInterval).toHaveBeenCalled();
            });

            it('should call once to the ajax service', function() {
                sut.switchPlan();
                expect(sut.ajaxService.ok.calls.count()).toBe(1)
            });

            it('should call the ajax service with parameters', function () {
                sut.switchPlan();
                expect(sut.ajaxService.ok.calls.allArgs()).toEqual([
                    ['GET', 'plan_url?type=pro&interval=annually']
                ]);
            });

            it('should return an updated plan', function() {
                var actual = sut.switchPlan().getActualResult();
                var expected = {
                    type: 'pro', interval: 'annually', amount: 5.0, dueDate: '2015-01-01',
                    switchType: spy, switchInterval: spy
                };
                expect(actual).toEqual(expected);

            });

        })

    });
});
