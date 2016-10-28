/**
 * Created by apium on 31/03/2016.
 */
define(function(require) {
    var path = 'controllers/costing/CostingCtrl';
    describe(path, function() {
        var Controller = require('controllers/costing/CostingCtrl');

        var sut, model, view, presenter, $scope, localStorage;
        beforeEach(function() {
            window.USER_TYPE = '';
            model = view = $scope = localStorage = {};
            presenter = {show: function() {}};
            sut = Controller.newInstance($scope, presenter, model, localStorage);
            sut.$scope = {
                events: {
                    onDeleteGenericItem: jasmine.createSpy(),
                    onDeleteCustomItem: jasmine.createSpy()
                }
            }
        });

        describe('onDelete', function() {

            describe('delete generic item', function() {

                beforeEach(function() {
                    sut.deleteItem = {
                        generic_table_row_id: 1
                    };
                    sut.onDelete();
                });

                it('should call onDeleteGenericItem function', function() {
                    expect(sut.$scope.events.onDeleteGenericItem).toHaveBeenCalledWith(1);
                });

                it('should not call onDeleteCustomItem function', function() {
                    expect(sut.$scope.events.onDeleteCustomItem).not.toHaveBeenCalled();
                });

            });

            describe('delete custom item', function() {

                beforeEach(function() {
                    sut.deleteItem = {
                        generic_table_row_id: null,
                        custom_id: 1
                    };
                    sut.onDelete();
                });

                it('should call onDeleteCustomItem function', function() {
                    expect(sut.$scope.events.onDeleteCustomItem).toHaveBeenCalledWith(1);
                });

                it('should not call onDeleteGenericItem function', function() {
                    expect(sut.$scope.events.onDeleteGenericItem).not.toHaveBeenCalled();
                });

            });

        });

    });
});