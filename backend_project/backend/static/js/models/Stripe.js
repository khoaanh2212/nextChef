;(function(app, window) {
    'use strict';

    var deps = [];
    function Factory() { return Stripe; }
    app.factory('Stripe', deps.concat([Factory]));
    if (window.define) define(deps, Factory);

    function Stripe(cardNumber, cardCVC, cardExpiryMonth, cardExpiryYear, stripe) {
        this.cardNumber = cardNumber;
        this.cardCVC = cardCVC;
        this.cardExpiryMonth = cardExpiryMonth;
        this.cardExpiryYear = cardExpiryYear;
        this.errors = [];
        this._stripe = stripe;
    }

    Stripe.StripeError = StripeError;

    Stripe.prototype.validate = function () {
        return (this.validateCardNumber() + this.validateCVC() + this.validateExpiry() == 3);
    };

    Stripe.prototype.validateCardNumber = function () {
        var valid = this._stripe.card.validateCardNumber(this.cardNumber);
        var error = new StripeError('card-number', 'Credit card number is invalid');
        if (!valid) {
            this.addError(error);
        } else this.removeError(error);
        return valid;
    };

    Stripe.prototype.validateCVC = function () {
        var valid = this._stripe.card.validateCVC(this.cardCVC);
        var error = new StripeError('card-cvc', 'Credit card CVC is invalid');
        if (!valid) {
            this.addError(error)
        } else this.removeError(error);
        return valid;
    };

    Stripe.prototype.validateExpiry = function () {
        var valid = this.cardExpiryYear && this.cardExpiryYear.length === 4 && this._stripe.card.validateExpiry(this.cardExpiryMonth, this.cardExpiryYear);
        var error = new StripeError('card-expiry', 'Credit card expiration date is invalid (MM/YYYY)');
        if (!valid) {
            this.addError(error)
        } else this.removeError(error);
        return valid;
    };

    Stripe.prototype.createToken = function (callback) {
        this._stripe.card.createToken({
            number: this.cardNumber,
            cvc: this.cardCVC,
            exp_month: this.cardExpiryMonth,
            exp_year: this.cardExpiryYear
        }, callback);
    };

    Stripe.prototype.addError = function (error) {
        if (!this.errors.some(function (e) {
                return e.code == error.code;
            })) {
            this.errors.push(error);
        }
    };

    Stripe.prototype.removeError = function(error) {
        this.errors = this.errors.filter(function(e) {
            return e.code !== error.code;
        });
    };

    Stripe.prototype.getErrors = function () {
        return this.errors;
    };

    Stripe.prototype.setCardNumber = function(cardNumber) {
        this.cardNumber = cardNumber;
    };

    Stripe.prototype.setCardCVC = function(cardCVC) {
        this.cardCVC = cardCVC;
    };

    Stripe.prototype.setCardExpiryMonth = function(cardExpiryMonth) {
        this.cardExpiryMonth = cardExpiryMonth;
    };

    Stripe.prototype.setCardExpiryYear = function(cardExpiryYear) {
        this.cardExpiryYear = cardExpiryYear;
    };

    Stripe.newInstance = function (cardNumber, cardCVC, cardExpiryMonth, cardExpiryYear, stripe) {
        return new Stripe(
            cardNumber || '',
            cardCVC || '',
            cardExpiryMonth || '',
            cardExpiryYear || '',
            stripe || _Stripe);
    };

    function StripeError(code, msg) {
        this.code = code;
        this.msg = msg;
    }

})(app, this);
