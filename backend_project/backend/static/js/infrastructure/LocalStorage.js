/**
 * Created by apium on 18/03/2016.
 */
;(function(app, window) {
    'use strict';

    var name = 'infrastructure/LocalStorage';
    var deps = [];
    function Factory() { return LocalStorage; }
    app.factory(name, deps.concat([Factory]));
    if (window.define) define(deps, Factory);

    function LocalStorage(context) {
        this.context = context;
    }

    LocalStorage.newInstance = function(context) {
        return new LocalStorage(context || window);
    };

    LocalStorage.prototype.set = function(name, data) {
        this.context.localStorage[name] = JSON.stringify(data);
    };

    LocalStorage.prototype.get = function(name) {
        try {
            return JSON.parse(this.context.localStorage[name]);
        } catch (error) {
            return this.context.localStorage[name];
        }
    };

    LocalStorage.prototype.remove = function(name) {
        try {
            return this.context.localStorage.removeItem(name);
        } catch (error) {
            return;
        }
    };

})(app, this);
