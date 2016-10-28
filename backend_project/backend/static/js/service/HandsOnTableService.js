/**
 * Created by apium on 24/05/2016.
 */
;(function (app, window) {
    'use strict';

    app.factory('HandsOnTableService', Factory);

    function Factory() {
        return HandsOnTableService;
    }

    function HandsOnTableService(handsOnTable) {
        this.handsOnTable = handsOnTable;
    }

    HandsOnTableService.newInstance = function () {
        return {
            new: function (hotElement, hotSettings) {
                var instance = new Handsontable(hotElement, hotSettings);
                return new HandsOnTableService(instance);
            }
        };
    };

    HandsOnTableService.prototype.getTable = function () {
        return this.handsOnTable;
    };
})(app, this);