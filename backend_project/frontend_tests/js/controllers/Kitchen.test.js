define(function(require) {
    describe('controllers/BookSlideOnKitchenController', function() {
        var BookSlideOnKitchenCtrl = require('controllers/BookSlideOnKitchenCtrl');
        var sut;
        beforeEach((function() {
            var addBook = {
              id: -1000,
              name: '+ add book'
            };
            sut = BookSlideOnKitchenCtrl.newInstance(addBook);
        }));

    });
});
