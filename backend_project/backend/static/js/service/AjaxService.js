/**
 * Created by Kate on 3/23/16.
 */

;(function (app, window) {
    'use strict';

    var deps = ['$q'];

    app.factory('AjaxService', Factory);

    function Factory(Q) {
        AjaxService.Q = Q;
        return AjaxService;
    }

    Factory.$inject = deps;

    function AjaxService(Q, $) {
        this.Q = Q;
        this.$ = $;
    }

    AjaxService.prototype.rest = function (method, path, data, options) {
        var ajaxCall = this._ajax(method, path, data, options);
        return this.Q.promise(function (resolve) {
            function resolveJqXHR(jqXHR) {
                delete jqXHR.then;
                resolve(jqXHR);
            }

            ajaxCall.then(function (data, textStatus, jqXHR) {
                resolveJqXHR(jqXHR);
            }, resolveJqXHR);
        });
    };

    AjaxService.prototype.ok = function (method, path, data, options) {
        return this.Q.all(this._ajax(method, path, data, options))
            .catch(this._rethrowAjaxError.bind(this));
    };

    AjaxService.prototype._ajax = function (method, path, data, options) {
        var params = this._prepareParams(method, path, data, options);
        return this.$.ajax(params);
    };

    AjaxService.prototype._prepareParams = function (method, path, data, options) {
        var params = options || {};
        options = options || {};
        params.dataType = options.dataType || "json";
        params.contentType = options.contentType || "application/json";
        params.url = path;
        params.type = method;
        params.cache = options.cache || false;
        params.timeout = options.timeout || 10000;
        params.beforeSend = this._beforeSend.bind(this);

        if (data) {
            params.data = (typeof data == 'string' || data instanceof String) ? data : JSON.stringify(data);
        }

        return params;
    };

    AjaxService.prototype._rethrowAjaxError = function (jqXHR, textStatus, errorThrown) {
        throw {
            status: jqXHR.status,
            responseText: jqXHR.responseText,
            textStatus: textStatus,
            errorThrown: errorThrown
        };
    };

    AjaxService.newInstance = function (Q, $) {
        Q = Q || AjaxService.Q;
        $ = $ || jQuery;
        var instance = new AjaxService(Q, $);
        return instance;
    };

    AjaxService.prototype._getCookie = function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    AjaxService.prototype._beforeSend = function (xhr, settings) {
        var csrftoken = this._getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    };

})(app, this);