/**
 * Created by apium on 24/03/2016.
 */
;(function (app, window) {
    var deps = ['$http', '$q'];

    function Factory($http, $q) {
        CostingModel.$http = $http;
        CostingModel.$q = $q;
        return CostingModel;
    }

    app.service('CostingModel', Factory);
    if (window.define) define(Factory);
    Factory.$inject = deps;

    function CostingModel($http, $q) {
        this.$http = $http;
        this.$q = $q;
        this.costingTable = [];
    }

    CostingModel.newInstance = function ($http, $q) {
        return new CostingModel(
            $http || CostingModel.$http,
            $q || CostingModel.$q
        );
    };

    CostingModel.prototype.getCostingTable = function () {
        return this.$http.get('/0/costing-list').then(function (response) {
            this.setCostingTable(response.data);
            return this.costingTable;
        }.bind(this));
    };

    CostingModel.prototype.setCostingTable = function (table) {
        this.costingTable = table;
    };

    CostingModel.prototype.delete = function (args) {
        var doDelete = this.$http.delete('/0/custom-ingredient?id=' + args.id);
        var doUpdate = this.$http.delete('/0/costing-generic-ingredient?id=' + args.genericIngredientId);
        return this.$q.all([doDelete, doUpdate]);
    };

    CostingModel.prototype.updateIngredientItem = function (args) {
        return this.$http.post('/0/costing-generic-ingredient',args).then(function (response) {
            return response;
        });
    };

    CostingModel.prototype.deleteGenericItem = function (id) {
        return this.$http.delete('/0/costing-generic-ingredient?id=' + id);
    };

    CostingModel.prototype.deleteCustomItem = function (id) {
        return this.$http.delete('/0/custom-ingredient?id=' + id);
    };

    CostingModel.prototype.duplicate = function (costing) {
        return (this.isGenericItem(costing)
            ? this.$http.put('/0/duplicate-ingredient?id=' + costing.generic_table_row_id)
            : this.$http.post('/0/duplicate-ingredient?id=' + costing.custom_id))
            .then(this.getCostingTable.bind(this));
    };

    CostingModel.prototype.isGenericItem = function (costing) {
        return !costing.custom_id;
    };

})(app, this);