/**
 * Created by apium on 24/03/2016.
 */
;(function (app, window) {
    var deps = ['$http'];

    function Factory($http) {
        CostingAddModel.$http = $http;
        return CostingAddModel;
    }

    app.service('CostingAddModel', Factory);
    if (window.define) define(Factory);
    Factory.$inject = deps;

    function CostingAddModel($http) {
        this.$http = $http;
    }

    CostingAddModel.newInstance = function ($http) {
        return new CostingAddModel($http || CostingAddModel.$http);
    };

    CostingAddModel.prototype.save = function (body) {
        return this.$http.post('/0/custom-ingredient', body);
    };

    CostingAddModel.prototype.calculateNetPrice = function(context) {
        if (!context.grossPrice || !context.waste
            || isNaN(context.grossPrice)
            || isNaN(context.waste)
            || context.waste === 100) {
            return {error: true};
        }
        return {
            netPrice: Math.round((100 * context.grossPrice)/(100 - context.waste) * 100) / 100,
            error: false
        };
    };

})(app, this);