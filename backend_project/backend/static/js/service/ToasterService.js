/**
 * Created by Kate on 3/24/16.
 */
;(function(app, window) {

    'use strict';

    app.factory('ToasterService', Factory);

    function Factory() {
        return ToasterService;
    }

    function ToasterService() {
        this.data = this.data || {};
    }

    ToasterService.prototype._initErrorAlertData = function() {
        this.data.listErrors = [];
        this.data.alert = {};
    };

    ToasterService.prototype.addError = function(err) {
        var newError = {msg: err, created: new Date()};
        this.data.listErrors.push(newError);
    };

    ToasterService.prototype.showAlert = function(error) {
        var now = new Date();
        this.data.listErrors = this.data.listErrors.filter(function(err) {
            return now.getSeconds() - err.created.getSeconds() < 2;
        });
        this._showBlockElements();
        return now.getSeconds() - error.created.getSeconds() < 2;
    };

    ToasterService.prototype._showBlockElements = function() {
        $('.block-alert .displayed').each(function() {
            var self = $(this);
            setTimeout(function() {
                self.removeClass('displayed');
            }, 3000);
        });
    };

    ToasterService.prototype.addAlert = function(object) {
        this.data.alert = {msg: object.msg, type: object.type};
    };

    ToasterService.prototype.sendAlert = function(object) {
        this.addAlert(object);

        var alert = $('#block-message');
        alert.stop().show().delay(3000).fadeOut('fast');
    };

    ToasterService.prototype.closeAlert = function() {
        $('#block-message').stop().fadeOut('fast');
    };

    ToasterService.newInstance = function() {
        return new ToasterService();
    }

}) (app, this);