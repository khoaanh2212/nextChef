define(function(require) {
    describe('models/Stripe', function() {
        var Stripe = require('models/Stripe');

        var sut, stripeStub;
        beforeEach(function() {
            stripeStub = {};
            sut = Stripe.newInstance(1,2,3,4, stripeStub);
        });

        describe('addError', function() {
            it('should add an error', function() {
                var error = new Stripe.StripeError('card-number', 'Credit card number is invalid');
                sut.addError(error);
                expect(sut.getErrors()).toEqual([error]);
            });
        });
    });
});
