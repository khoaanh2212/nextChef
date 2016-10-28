/**
 * Created by apium on 24/03/2016.
 */
define(function (require) {
    var path = 'controllers/BookModalCtrl';

    describe(path, function () {
        var Controller = require('controllers/BookModalCtrl');

        var sut, scope = {}, timeout = {}, model = {}, presenter = {
            show: function () {
            }
        }, $http = {};

        beforeEach(function () {
            sut = Controller.newInstance(scope, presenter, model, timeout, $http);
            sut.$scope.events = {};
        });

        describe('fn', function () {
            var expected = ['loadMoreCollaborator', 'getCollaborator', 'selectCollaborator', 'onCancelEdit', 'onUpdateBook'];
            describe('always', function () {
                it('should define expected properties in fn', function () {
                    sut.subcribeEditBoot = jasmine.createSpy();
                    var actual = Object.keys(sut.$scope.fn);
                    // expect(actual).toEqual(expected);
                });

                it('should define only functions', function () {
                    var fn = sut.$scope.fn;
                    Object.keys(fn).forEach(function (key) {
                        // expect(typeof fn[key]).toBe('function');
                    });
                });
            });
        });

        describe('init', function () {
            it('should call init default modal', function () {
                var actual = spyOn(sut, 'initDefaultModal');
                sut.$scope.$on = jasmine.createSpy();
                sut.init();
                expect(actual).toHaveBeenCalledWith();
            });

            it('should set default book', function () {
                var expected = {
                    name: '',
                    private: 0,
                    collaborators: []
                };
                sut.init();
                expect(sut.$scope.book).toEqual(expected);
            });
        });

        describe('initBookToList', function () {
            it('should publish event', function () {
                var actual = sut.$scope.$emit = jasmine.createSpy();
                sut.initBookToList({data: {}});
                expect(actual).toHaveBeenCalledWith('addingBookToSlide', {});
            });
        });

        describe('initCollaboratorDropdown', function () {

            var response;

            beforeEach(function () {
                sut.$scope = {
                    collaborators: {}, isShowCollaboratorDropdown: false, collaboratorDropdownPaging: 0
                };
                response = {
                    chefs: [], readmore: true
                };
            });

            it('should assign the response to collaborators', function () {
                sut.initCollaboratorDropdown(response);
                expect(sut.$scope.collaborators.chefs).toEqual([]);
                expect(sut.$scope.collaborators.readmore).toBeTruthy();
            });

            it('should set the page as \'1\' if collaboratorDropdownPaging is not set', function () {
                sut.$scope.collaboratorDropdownPaging = undefined;
                sut.initCollaboratorDropdown(response);
                expect(sut.$scope.collaboratorDropdownPaging).toEqual(1);
            });

            it('should re-set the page as \'1\' if collaboratorDropdownPaging is set', function () {
                sut.$scope.collaboratorDropdownPaging = 5;
                sut.initCollaboratorDropdown(response);
                expect(sut.$scope.collaboratorDropdownPaging).toEqual(5);
            });

            it('should show dropdown', function () {
                sut.initCollaboratorDropdown(response);
                expect(sut.$scope.isShowCollaboratorDropdown).toBeTruthy();
            });

        });

        describe('loadMoreCollaborator', function () {
            it('should call to onChangeGetCollaborator', function () {
                sut.$scope.events.onChangeGetCollaborator = jasmine.createSpy();
                sut.loadMoreCollaborator('name', 1);
                expect(sut.$scope.events.onChangeGetCollaborator).toHaveBeenCalledWith('name', 2);
            });
        });

        describe('selectCollaborator', function () {

            describe('always', function () {
                it('should close the dropdown list', function () {
                    sut.$scope.isShowCollaboratorDropdown = true;
                    sut.selectCollaborator({});
                    expect(sut.$scope.isShowCollaboratorDropdown).toBeFalsy();
                });

                it('should reset the input', function () {
                    sut.$scope.colaborator_name = 'chef-01';
                    sut.selectCollaborator({});
                    expect(sut.$scope.colaborator_name).toBeUndefined();
                });
            });

            describe('collaborator is not added', function () {
                it('should update the list of collaborator', function () {
                    var collaborator = {email: 'first@mail.com'};
                    sut.$scope.book.collaborators = [
                        {email: 'third@mail.com'}, {email: 'second@mail.com'}
                    ];
                    sut.selectCollaborator(collaborator);
                    expect(sut.$scope.book.collaborators).toEqual([
                        {email: 'third@mail.com'}, {email: 'second@mail.com'}, {email: 'first@mail.com'}
                    ])
                });
            });

            describe('collaborator is added', function () {
                it('should not update the list of collaborator', function () {
                    var collaborator = {email: 'first@mail.com'};
                    sut.$scope.book.collaborators = [
                        {email: 'first@mail.com'}, {email: 'second@mail.com'}
                    ];
                    sut.selectCollaborator(collaborator);
                    expect(sut.$scope.book.collaborators).toEqual([
                        {email: 'first@mail.com'}, {email: 'second@mail.com'}
                    ])
                });
            });

        });

    });
});