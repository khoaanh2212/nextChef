define(function (require) {

    describe('CookboothCtrl', function () {

        var CookboothCtrl = require('controllers/CookboothCtrl');
        var PromiseHelper = require('../../test-helpers/Promise.js');

        var sut;

        beforeEach(function () {
            $scope = {};
            $compile = {};
            $timeout = jasmine.createSpy().and.callFake(function () {
            });
            Tooltip = {};
            KitchenTooltipStorage = {};
            sut = CookboothCtrl.newInstance($scope, $compile, $timeout, Tooltip, KitchenTooltipStorage);
            sut.ga = jasmine.createSpy().and.callFake(function () {
            });
        });

        describe('fn', function () {
            var expected = ['init', 'setCookie', 'reposition', 'sendGoogleAnalyticsPageView',
                'checkAuthenticated', 'setAccountModalType', 'showLoginPopup', 'configModalWhenShowLoginPopup',
                'showJoinPopup', 'showRegisterPopupWithEmail', 'showRegisterPopup', 'configModalWhenShowJoinPopup', 'emailAccount', 'selectLoginForm',
                'selectJoinForm', 'facebookCheck', 'facebookConnect', 'openTooltip', 'adjustTooltipOffset',
                'closeTooltip', 'initTooltip', 'getTooltipHtml', 'saveClosedTooltip', 'getClosedTooltip', 'showConversionPopup', 'validationRegister'];
            describe('always', function () {
                it('should define expected properties in fn', function () {
                    var actual = Object.keys(sut.$scope.fn);
                    expect(actual).toEqual(expected);
                });

                it('should define only functions', function () {
                    var fn = sut.$scope.fn;
                    Object.keys(fn).forEach(function (key) {
                        expect(typeof fn[key]).toBe('function');
                    });
                });
            });
        });

        describe('checkAuthenticated', function () {
            describe('set accountModalType ', function () {
                var test = [
                    {
                        name: 'kitchen',
                        type: 1
                    },
                    {
                        name: 'recipe',
                        type: 1
                    },
                    {
                        name: 'follow',
                        type: 2
                    },
                    {
                        name: 'chefs',
                        type: 3
                    },
                    {
                        name: 'add',
                        type: 4
                    },
                    {
                        name: 'love',
                        type: 5
                    },
                    {
                        name: 'comment',
                        type: 1
                    }
                ];
                test.forEach(function (model) {
                    it('should set type correct', function () {
                        sut.$scope.fn.setAccountModalType(model.name);
                        expect(sut.$scope.accountModalType).toBe(model.type);
                    });
                });
            });
        });
        describe('show login popup', function () {
            describe('configModalWhenShowLoginPopup', function () {
                it('should change tab modal type to login tab', function () {
                    sut.$scope.fn.configModalWhenShowLoginPopup();
                    expect(sut.$scope.accountModalTab).toEqual(sut.$scope.accountModalLoginTab);
                });
                it('should send to ga message that account popup show', function () {
                    var sendGoogleAnalyticsPageViewSpy = sut.$scope.fn.sendGoogleAnalyticsPageView = jasmine.createSpy();
                    sut.$scope.fn.configModalWhenShowLoginPopup();
                    expect(sendGoogleAnalyticsPageViewSpy).toHaveBeenCalledWith('/account-popup/show');
                });
            });
        });
        describe('show join popup', function () {
            describe('configModalWhenShowJoinPopup', function () {
                it('should change tab modal type to join tab', function () {
                    sut.$scope.fn.configModalWhenShowJoinPopup();
                    expect(sut.$scope.accountModalTab).toEqual(sut.$scope.accountModalJoinTab);
                });
                it('should send to ga message that account popup show', function () {
                    var sendGoogleAnalyticsPageViewSpy = sut.$scope.fn.sendGoogleAnalyticsPageView = jasmine.createSpy();
                    sut.$scope.fn.configModalWhenShowJoinPopup();
                    expect(sendGoogleAnalyticsPageViewSpy).toHaveBeenCalledWith('/account-popup/show');
                });
            });
        });
        describe('user choose login with eamil account', function () {
            it('should change modal status to email status', function () {
                sut.$scope.fn.emailAccount();
                expect(sut.$scope.accountModalStatus).toEqual(sut.$scope.accountModalEmailStatus);
            });
            it('should send to ga message that email connect', function () {
                var sendGoogleAnalyticsPageViewSpy = sut.$scope.fn.sendGoogleAnalyticsPageView = jasmine.createSpy();
                sut.$scope.fn.emailAccount();
                expect(sendGoogleAnalyticsPageViewSpy).toHaveBeenCalledWith('/account-popup/email-connect');
            });
            it('should send to ga message that user want to join(with email) if user is on join tab', function () {
                var sendGoogleAnalyticsPageViewSpy = sut.$scope.fn.sendGoogleAnalyticsPageView = jasmine.createSpy();
                sut.$scope.accountModalTab = sut.$scope.accountModalJoinTab;
                sut.$scope.fn.emailAccount();
                expect(sendGoogleAnalyticsPageViewSpy).toHaveBeenCalledWith('/account-popup/join-form');
            });
            it('should send to ga message that user want to login(with email) if user is not on join tab', function () {
                var sendGoogleAnalyticsPageViewSpy = sut.$scope.fn.sendGoogleAnalyticsPageView = jasmine.createSpy();
                sut.$scope.accountModalTab = sut.$scope.accountModalJoinTab + 1000;
                sut.$scope.fn.emailAccount();
                expect(sendGoogleAnalyticsPageViewSpy).toHaveBeenCalledWith('/account-popup/login-form');
            });
        });
        describe('facebook', function () {
            describe('facebook checking', function () {
            });
        });
    });

});