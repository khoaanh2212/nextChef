define(function(require) {
    describe('models/Plan', function() {
        var Plan = require('models/Plan');

        var sut;
        beforeEach(function() {
            planType = 'pro';
            planInterval = 'monthly';
            amount = 5.90;
            dueDate = 'dueDate';
            sut = Plan.newInstance(planType, planInterval, amount, dueDate);
        });

        describe('getNextType', function() {
            it('should return next type', function() {
                sut.type = 'business';
                actual = sut.getNextType();
                expect(actual).toEqual('pro');
            });
        });

        describe('getNextInterval', function() {
            it('should return next interval', function() {
                sut.interval = 'monthly';
                actual = sut.getNextInterval();
                expect(actual).toEqual('annually');
            });
        });

        describe('switchType', function() {
            it('should switch current type', function() {
                sut.type = 'pro';
                sut.switchType();
                expect(sut.type).toEqual('business');
                expect(sut.nextType).toEqual('pro');
            })
        });

        describe('switchInterval', function() {
            it('should switch current interval', function() {
                sut.type = 'monthly';
                sut.switchInterval();
                expect(sut.interval).toEqual('annually');
                expect(sut.nextInterval).toEqual('monthly');
            })
        });

    });
});
