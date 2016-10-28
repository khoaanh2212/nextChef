;(function (app, window) {
    'use strict';
    app.factory('BookSlideOnKitchenController', [function() {
        return BookSlide;
    }]);

    if (window.define) define(function (require) {
        return BookSlide;
    });

    function BookSlide() {
        this.bookSlides = [];
        this.booksPerSlide = 8;
    }

    BookSlide.prototype.createBookSlide = function(booklist) {
        for (var i = 0; i < booklist.length; i = i + this.booksPerSlide) {
            var slide = [];
            for (var j = 0; j < this.booksPerSlide && i + j < booklist.length; j++) {
                slide.push(booklist[i + j]);
            }
            this.bookSlides.push(slide);
        }
        this.initAddButton();
    };

    BookSlide.prototype.addNewBook = function(book) {
        this.removeAddButton();
        this.addNewBookToSlide(book);
        this.initAddButton();
    };

    BookSlide.prototype.addNewBookToSlide = function(book) {
        if (this.bookSlides.length == 0) {
            this.bookSlides.push([book]);
        } else {
            var lastSlide = this.bookSlides[this.bookSlides.length - 1];
            if (lastSlide.length == this.booksPerSlide) {
                this.bookSlides.push([book]);
            } else {
                lastSlide.push(book);
            }
        }
    };

    BookSlide.prototype.initAddButton = function() {
        this.addNewBookToSlide({
            id: -1,
            name: '+ add book'
        });
    };

    BookSlide.prototype.removeAddButton = function() {
        this.bookSlides[this.bookSlides.length - 1].pop();
    };

    BookSlide.prototype.isBook = function(book){
        return (book.id >= 0);
    };

    BookSlide.newInstance = function() {
        return new BookSlide();
    }

})(app, this);