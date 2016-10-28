;(function (app, window) {
    'use strict';

    var deps = ['$scope', '$compile', '$timeout', 'domain/kitchen/TutorialTooltip', 'infrastructure/KitchenTooltipStorage', '$http'];

    app.controller("CookboothCtrl", deps.concat([function ($scope, $compile, $timeout, Tooltip, KitchenTooltipStorage, $http) {
        CookboothCtrl.$scope = $scope;
        CookboothCtrl.$compile = $compile;
        CookboothCtrl.$timeout = $timeout;
        CookboothCtrl.Tooltip = Tooltip;
        CookboothCtrl.$http = $http;
        CookboothCtrl.KitchenTooltipStorage = KitchenTooltipStorage;
        return CookboothCtrl.newInstance();
    }]));

    if (window.define) define(function () {
        return CookboothCtrl;
    });

    function CookboothCtrl($scope, $compile, $timeout, Tooltip, KitchenTooltipStorage, $http) {
        $scope.ACCOUNTMODELTYPE = [
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
        $scope.accountModalType = 4;
        $scope.accountModalMainStatus = 1;
        $scope.accountModalEmailStatus = 2;
        $scope.accountModalLoginTab = 1;
        $scope.accountModalJoinTab = 2;
        $scope.accountModalTab = $scope.accountModalJoinTab;
        $scope.accountModalStatus = $scope.accountModalMainStatus;
        this.$scope = $scope;

        this.$compile = $compile;
        this.$timeout = $timeout;
        this.Tooltip = Tooltip;
        this.$http = $http;
        this.KitchenTooltipStorage = KitchenTooltipStorage;

        this._initFn();

        this.$scope.fn.init();
    }

    CookboothCtrl.prototype._initFn = function () {
        this.$scope.fn = {
            init: this.init.bind(this),
            setCookie: this.setCookie.bind(this),
            reposition: this.reposition.bind(this),
            sendGoogleAnalyticsPageView: this.sendGoogleAnalyticsPageView.bind(this),
            checkAuthenticated: this.checkAuthenticated.bind(this),
            setAccountModalType: this.setAccountModalType.bind(this),
            showLoginPopup: this.showLoginPopup.bind(this),
            configModalWhenShowLoginPopup: this.configModalWhenShowLoginPopup.bind(this),
            showJoinPopup: this.showJoinPopup.bind(this),
            showRegisterPopupWithEmail: this.showRegisterPopupWithEmail.bind(this),
            showRegisterPopup: this.showRegisterPopup.bind(this),
            configModalWhenShowJoinPopup: this.configModalWhenShowJoinPopup.bind(this),
            emailAccount: this.emailAccount.bind(this),
            selectLoginForm: this.selectLoginForm.bind(this),
            selectJoinForm: this.selectJoinForm.bind(this),
            facebookCheck: this.facebookCheck.bind(this),
            facebookConnect: this.facebookConnect.bind(this),
            openTooltip: this.openTooltip.bind(this),
            adjustTooltipOffset: this.adjustTooltipOffset.bind(this),
            closeTooltip: this.closeTooltip.bind(this),
            initTooltip: this.initTooltip.bind(this),
            getTooltipHtml: this.getTooltipHtml.bind(this),
            saveClosedTooltip: this.saveClosedTooltip.bind(this),
            getClosedTooltip: this.getClosedTooltip.bind(this),
            showConversionPopup: this.showConversionPopup.bind(this),
            validationRegister: this.validationRegister.bind(this)
        };
    };

    CookboothCtrl.prototype.init = function () {
        var self = this;
        this.$scope.bii = false;
        $('.modal').on('show.bs.modal', this.$scope.reposition);
        $(window).on('resize', function () {
            //$('.modal:visible').each(this.$scope.reposition);
            self.$scope.fn.initTooltip();
        });
        this.$timeout(function () {
            this.$scope.fn.initTooltip();
        }.bind(this), 10, false);
    };

    CookboothCtrl.prototype.setCookie = function (cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + "; " + expires;
    };

    CookboothCtrl.prototype.reposition = function () {
        var modal = $(this),
            dialog = modal.find('.modal-dialog');
        modal.css('display', 'block');

        // Dividing by two centers the modal exactly, but dividing by three
        // or four works better for larger screens.
        dialog.css("margin-top", Math.max(0, ($(window).height() - dialog.height()) / 2));
    };

    CookboothCtrl.prototype.sendGoogleAnalyticsPageView = function (page) {
        if (typeof this.ga != 'undefined')
            this.ga('aloneTracker.send', 'pageview', page);
    };

    CookboothCtrl.prototype.checkAuthenticated = function (text) {

        this.$scope.accountModalStatus = this.$scope.accountModalMainStatus;

        var modal = $('#conversion_modal');
        this.$scope.fn.setAccountModalType(text);
        modal.modal('show');

        /*var modal = $('#account_modal');
         if(text=='add'){
         modal.find('h2').text('Add this recipe to your books?');
         modal.find('h2').show();
         modal.find('h3').hide();
         modal.find('p').show();
         modal.find('.recipe').hide();
         }else if(text=='comment'){
         modal.find('h2').text('Want to leave a comment?');
         modal.find('h2').show();
         modal.find('h3').hide();
         modal.find('p').show();
         modal.find('.recipe').hide();
         }else if(text=='love'){
         modal.find('h2').text('Love this recipe?');
         modal.find('h2').show();
         modal.find('h3').hide();
         modal.find('p').show();
         modal.find('.recipe').hide();
         }else if(text=='follow'){
         modal.find('h2').text('Want to follow chefs and foodies?');
         modal.find('h2').show();
         modal.find('h3').hide();
         modal.find('p').show();
         modal.find('.recipe').hide();
         }else if(text=='kitchen'){
         modal.find('h2').text('Creating your first recipe?');
         modal.find('h2').show();
         modal.find('h3').hide();
         modal.find('p').show();
         modal.find('.recipe').hide();
         }else if(text=='recipe'){
         modal.find('.recipe').text('You need to sign in to use all of NextChef.');
         modal.find('h2').hide();
         modal.find('p').hide();
         modal.find('.recipe').show();
         }
         modal.modal('show');
         */

        this.$scope.fn.sendGoogleAnalyticsPageView('/account-popup/show');
    };

    CookboothCtrl.prototype.setAccountModalType = function (text) {
        for (var i = 0; i < this.$scope.ACCOUNTMODELTYPE.length; i++) {
            if (this.$scope.ACCOUNTMODELTYPE[i].name == text) {
                this.$scope.accountModalType = this.$scope.ACCOUNTMODELTYPE[i].type;
                break;
            }
        }
    };

    CookboothCtrl.prototype.showLoginPopup = function () {
        var modal = $('#account_modal');
        modal.find('h3').hide();
        modal.find('p').show();
        modal.find('.recipe').hide();
        this.$scope.fn.configModalWhenShowLoginPopup();
        modal.modal('show');
    };

    CookboothCtrl.prototype.showConversionPopup = function () {
        var modal = $('#conversion_modal');
        modal.modal('show');
    };

    CookboothCtrl.prototype.showRegisterPopupWithEmail = function () {
        if (this.$scope.emailAddress.trim() != '') {
            this.$scope.accountModalStatus = this.$scope.accountModalEmailStatus;
            this.$scope.accountModalTab = this.$scope.accountModalJoinTab;
            $('input[name=email]').val(this.$scope.emailAddress);
            var modal = $('#account_modal');
            modal.modal('show');
        }
    }

    CookboothCtrl.prototype.showRegisterPopup = function () {
        this.$scope.accountModalStatus = this.$scope.accountModalEmailStatus;
        this.$scope.accountModalTab = this.$scope.accountModalJoinTab;
        var modal = $('#account_modal');
        modal.modal('show');
    }

    CookboothCtrl.prototype.configModalWhenShowLoginPopup = function () {
        this.$scope.accountModalStatus = this.$scope.accountModalMainStatus;
        this.$scope.accountModalTab = this.$scope.accountModalLoginTab;
        this.$scope.fn.sendGoogleAnalyticsPageView('/account-popup/show');
    };

    CookboothCtrl.prototype.showJoinPopup = function () {
        var modal = $('#account_modal');
        modal.find('h3').hide();
        modal.find('p').show();
        modal.find('.recipe').hide();
        this.$scope.fn.configModalWhenShowJoinPopup();
        modal.modal('show');
    };

    CookboothCtrl.prototype.configModalWhenShowJoinPopup = function () {
        this.$scope.accountModalStatus = this.$scope.accountModalMainStatus;
        this.$scope.accountModalTab = this.$scope.accountModalJoinTab;
        this.$scope.fn.sendGoogleAnalyticsPageView('/account-popup/show');
    };

    CookboothCtrl.prototype.emailAccount = function () {
        this.$scope.accountModalStatus = this.$scope.accountModalEmailStatus;
        this.$scope.fn.sendGoogleAnalyticsPageView('/account-popup/email-connect');
        if (this.$scope.accountModalTab == this.$scope.accountModalJoinTab) {
            this.$scope.fn.sendGoogleAnalyticsPageView('/account-popup/join-form');
        } else {
            this.$scope.fn.sendGoogleAnalyticsPageView('/account-popup/login-form');
        }
    };

    CookboothCtrl.prototype.selectLoginForm = function () {
        this.$scope.accountModalTab = this.$scope.accountModalLoginTab;
        this.$scope.fn.sendGoogleAnalyticsPageView('/account-popup/login-form');
    };

    CookboothCtrl.prototype.selectJoinForm = function () {
        this.$scope.accountModalTab = this.$scope.accountModalJoinTab;
        $('input[name=email]').val('');
        this.$scope.fn.sendGoogleAnalyticsPageView('/account-popup/join-form');
    };

    CookboothCtrl.prototype.facebookCheck = function () {
        FB.getLoginStatus(function (response) {
            // Check if is logged in FB
            if (response.status != 'connected') {
                FB.login(function (response) {
                    this.$scope.fn.facebookConnect(response);
                }, {
                    scope: 'email'
                });
            } else {
                this.$scope.fn.facebookConnect(response);
            }
        });
    };

    CookboothCtrl.prototype.facebookConnect = function (response) {

        this.$scope.fn.sendGoogleAnalyticsPageView('/account-popup/facebook-connect');

        var csrftoken = getCookie('csrftoken');
        if (response.authResponse) {
            FB.api('/me', function (meResponse) {
                var last_name;
                if (meResponse.middle_name) {
                    last_name = meResponse.middle_name + ' ' + meResponse.last_name;
                } else {
                    last_name = meResponse.last_name;
                }
                $('<form>').attr({
                    method: 'post', action: FACEBOOK_LOGIN_URL,
                }).append($('<input>').attr({
                    type: 'hidden', name: 'csrfmiddlewaretoken', value: csrftoken,
                })).append($('<input>').attr({
                    type: 'text', name: 'first_name', value: meResponse.first_name
                })).append($('<input>').attr({
                    type: 'text', name: 'last_name', value: last_name
                })).append($('<input>').attr({
                    type: 'text', name: 'email', value: meResponse.email
                })).append($('<input>').attr({
                    type: 'text', name: 'picture', value: 'https://graph.facebook.com/' + meResponse.id + '/picture'
                })).append($('<input>').attr({
                    type: 'text', name: 'user_id', value: response.authResponse.userID
                })).append($('<input>').attr({
                    type: 'text', name: 'token', value: response.authResponse.accessToken
                })).append($('<input>').attr({
                    type: 'text', name: 'male', value: (meResponse.gender == "male") ? 1 : 0
                })).append($('<input>').attr({
                    type: 'text', name: 'type', value: 0
                })).submit();
            });
        }
    };

    CookboothCtrl.prototype.openTooltip = function (tooltip_name, element_id, title, content, position, container) {
        var tooltipStorage = this.$scope.fn.getClosedTooltip();

        var tooltip_id = "tooltip-for-" + element_id;

        var options = {
            html: true,
            trigger: 'manual',
            title: '<div id="' + tooltip_id + '"></div>',
            placement: position,
            template: '<div class="tooltip cookbooth-tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
        };

        if (container) options.container = container;

        this.$element = $('#' + element_id);

        this.$element.tooltip(options);
        if (!tooltipStorage[element_id]) this.$element.tooltip('show');

        var $html = this.$scope.fn.getTooltipHtml(title, content, element_id, container);

        var temp = this.$compile($html)(this.$scope);
        angular.element(document.getElementById(tooltip_id)).append(temp);

        this.$scope.fn.adjustTooltipOffset(tooltip_name, container);

    };

    CookboothCtrl.prototype.adjustTooltipOffset = function (tooltip, container) {

        var offset = {
            left: {
                'PROFILE': -50, 'RECIPE': 15, 'MENU': -50
            },
            top: {
                'PROFILE': -93, 'RECIPE': 40, 'MENU': 0
            }
        };

        this.$tooltip = $(container + ' .tooltip');

        this.$tooltip.css('top', parseInt(this.$tooltip.css('top')) + offset['top'][tooltip] + 'px');
        this.$tooltip.css('left', parseInt(this.$tooltip.css('left')) + offset['left'][tooltip] + 'px');
    };

    CookboothCtrl.prototype.closeTooltip = function (element_id) {
        $('#' + element_id).tooltip('hide');
    };

    CookboothCtrl.prototype.initTooltip = function () {
        if (typeof window.BOOKS != 'undefined' && IS_AT_HOME) {
            if (window.BOOKS.length === 0) {
                this.$scope.fn.openTooltip('MENU', 'kitchen', 'Upload your first recipe', ' ', 'bottom', '#global_navbar');
                this.$scope.fn.openTooltip('RECIPE', 'library_recipe_title', 'Manage your recipes', ' ', 'right', 'li.recipes-list');
                this.$scope.fn.openTooltip('PROFILE', 'library_edit_profile', 'Edit your profile', ' ', 'top', '#library_edit_profile-tooltip-wrapper');
            }
        }
    };

    CookboothCtrl.prototype.getTooltipHtml = function (title, content, element_id) {
        var html = '';
        html += '<div class="next-chef-tooltip hidden-xs">';
        html += '<div class="tooltip-close" ng-click="fn.closeTooltip(\'' + element_id + '\'); fn.saveClosedTooltip(\'' + element_id + '\')"></div>';
        html += '<div class="tooltip-header">';
        html += '<h2>' + title + '</h2>';
        html += '</div>';
        html += '<div class="tooltip-content">' + content + '</div>';
        html += '</div>';
        return $(html);
    };

    CookboothCtrl.prototype.saveClosedTooltip = function (element_id) {
        var object = this.$scope.fn.getClosedTooltip();
        object[element_id] = true;
        this.KitchenTooltipStorage.newInstance().saveTutorial(CHEF_ID, this.Tooltip.newInstance(object));
    };

    CookboothCtrl.prototype.getClosedTooltip = function () {
        return this.KitchenTooltipStorage.newInstance().getTutorial(CHEF_ID).toDTO();
    };

    CookboothCtrl.newInstance = function ($scope, $compile, $timeout, Tooltip, KitchenTooltipStorage, $http) {
        $scope = $scope || CookboothCtrl.$scope;
        $compile = $compile || CookboothCtrl.$compile;
        $timeout = $timeout || CookboothCtrl.$timeout;
        Tooltip = Tooltip || CookboothCtrl.Tooltip;
        KitchenTooltipStorage = KitchenTooltipStorage || CookboothCtrl.KitchenTooltipStorage;
        $http = $http || CookboothCtrl.$http;
        var instance = new CookboothCtrl(
            $scope, $compile, $timeout, Tooltip, KitchenTooltipStorage, $http
        );

        return instance;
    };

    CookboothCtrl.prototype.validationRegister = function ($event) {
        var currentItem = $($event.currentTarget);
        var email = currentItem.parents('.form-parents').find('input[name="email"]').val().trim();
        var name = currentItem.parents('.form-parents').find('input[name="name"]').val().trim();
        var surname = currentItem.parents('.form-parents').find('input[name="surname"]').val().trim();

        var form = currentItem.parents('.form-parents');
        this.$scope.email_error = '';
        if(email=='' || name == '' || surname==''){
            form.find('button').click();
        }else{
            var body = {
                'email': email
            }
            if (email.trim() != '') {
                var $scope = this.$scope;
                this.$http.post('/accounts/register/validation/', body).then(function (response) {
                    if (response.data.valid) {
                        form.find('button').click();
                    } else {
                        $scope.email_error = 'This email address is already in use. Please supply a different email address.';
                        return false;
                    }
                });
            }
        }


    };
})(app, this);
