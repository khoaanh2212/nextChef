app.controller('LibraryController', ['$scope', 'Chef', function ($scope, Chef) {
    $scope.isUserAuthenticated = USER_AUTHENTICATED;
    $scope.userFollowsList = USER_FOLLOWS_LIST;
    $scope.userId = USER_ID;
    $scope.loadingAvatar = false;
    $scope.loadingRestaurant = false;
    $scope.loadingCover = false;
    $scope.restaurantActive = false;
    $scope.followersActive = false;
    $scope.followingActive = false;
    $scope.followersLoading = false;
    $scope.followingLoading = false;

    $scope.restaurantLoc = (RESTAURANT_LATITUDE != '') && (RESTAURANT_LONGITUDE != '');

    $scope.chef = new Chef({id: CHEF_ID});
    $scope.chef.checkFollowed($scope.userFollowsList);

    $scope.follow = function (chef) {

        if (!$scope.isUserAuthenticated) {
            checkAuthenticated('follow');
        } else {
            if (chef.followed) {
                chef.follow().then(function (recipesArray) {
                    chef.followed = false;
                    if (chef.id == CHEF_ID) $scope.followersCount--;
                });
            } else {
                chef.follow().then(function (recipesArray) {
                    chef.followed = true;
                    if (chef.id == CHEF_ID) $scope.followersCount++;
                });
            }
        }
    }

    $scope.saveProfile = function () {
        var enableSaveButton = $scope.checkChangePasswordCommit();
        if(!enableSaveButton)
            return false;
        var address = angular.element('#id_restaurant-address').val();
        //var city = angular.element('#id_restaurant-city').val();
        //var state = angular.element('#id_restaurant-state').val();
        //var country = angular.element('#id_restaurant-country').val();
        //var complete_address = address + ' ,' + city + ' ,' + state + ' ,' + country;

        var geocoder = new google.maps.Geocoder();
        geocoder.geocode({'address': address}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                result = results[0];
                for (var i = 0; i < result.address_components.length; i++) {
                    var component = result.address_components[i];
                    if (component.types.indexOf('country') != -1) {
                        angular.element('#id_restaurant-country').val(component.long_name);
                    } else if (component.types.indexOf('postal_code') != -1) {
                        angular.element('#id_restaurant-zip').val(component.long_name);
                    } else if (component.types.indexOf('administrative_area_level_1') != -1) {
                        angular.element('#id_restaurant-state').val(component.long_name);
                    } else if (component.types.indexOf('locality') != -1) {
                        angular.element('#id_restaurant-city').val(component.long_name);
                    }
                }
                var latitude = angular.copy(result.geometry.location.G);
                var longitude = angular.copy(result.geometry.location.K);
                angular.element('#id_restaurant-latitude').val(latitude);
                angular.element('#id_restaurant-longitude').val(longitude);

            } else {
                angular.element('#id_restaurant-latitude').val(0);
                angular.element('#id_restaurant-longitude').val(0);
            }
            angular.element('#save_profile_form').submit();

        });

        return false;
    };

    $scope.setRestaurantMap = function () {

        var map = document.getElementById('map_canvas');

        if (map != null) {
            var geocoder = new google.maps.Geocoder();
            var latitude = RESTAURANT_LATITUDE;
            var longitude = RESTAURANT_LONGITUDE;

            if (latitude != '' && longitude != '') {
                var stylez = [{
                    featureType: "all",
                    elementType: "all",
                    stylers: [{saturation: -100}]
                }];
                var latlng = new google.maps.LatLng(parseFloat(latitude), parseFloat(longitude));
                var mapOptions = {
                    zoom: 12,
                    center: latlng,
                    panControl: false,
                    zoomControl: true,
                    scaleControl: false,
                    streetViewControl: false,
                    overviewMapControl: false,
                    mapTypeControl: false,
                };
                var map = new google.maps.Map(map, mapOptions);
                map.setOptions({styles: stylez});
                var marker = new google.maps.Marker({
                    map: map,
                    position: new google.maps.LatLng(parseFloat(latitude), parseFloat(longitude))
                });
            }
        }
    };

    $scope.setRestaurantMap();

    $scope.uploadRestaurantImage = function (files) {
        $scope.loadingRestaurant = true;
        $scope.chef.uploadRestaurantImage(files[0]).then(function (result) {
            if (result.data.success) {
                $('#library_modal_restaurant_image').attr('src', result.data.url);
            }
            $scope.loadingRestaurant = false;
        });
    };

    $scope.uploadAvatarImage = function (files) {
        $scope.loadingAvatar = true;
        $scope.chef.uploadAvatarImage(files[0]).then(function (result) {
            if (result.data.success) {
                $('#library_modal_avatar').attr('src', result.data.url);
            }
            $scope.loadingAvatar = false;
        });
    };

    $scope.uploadCoverImage = function (files) {
        $scope.loadingCover = true;
        $scope.chef.uploadCoverImage(files[0]).then(function (result) {
            if (result.data.success) {
                $('#library_modal_cover').attr('src', result.data.url);
            }
            $scope.loadingCover = false;
        });
    };

    $scope.showFollowers = function () {
        if ($scope.followersActive == false) {
            $scope.followingActive = false;
            $scope.followersActive = true;
            if ($scope.chef.followers == undefined) {
                $scope.followersLoading = true;
                $scope.chef.loadFollowers($scope.userFollowsList).then(function (result) {
                    $scope.followersLoading = false;
                });
            }
        }
        else {
            $scope.followersActive = false;
        }
    };

    $scope.showFollowing = function () {
        if ($scope.followingActive == false) {
            $scope.followersActive = false;
            $scope.followingActive = true;
            if ($scope.chef.following == undefined) {
                $scope.followingLoading = true;
                $scope.chef.loadFollowing($scope.userFollowsList).then(function (result) {
                    $scope.followingLoading = false;
                });
            }
        }
        else {
            $scope.followingActive = false;
        }
    }

    $scope.updateTitleChangePassword = function () {
        $scope.showChangePassword = !$scope.showChangePassword;
        $scope.change_password_title = $scope.showChangePassword ? 'Hide change password' : 'Change password';
    };

    $scope.validateNewPassword = function () {
        if ($scope.new_password != $scope.confirm_password && ($scope.new_password != '' || $scope.confirm_password != '')) {
            $('.lblConfirmPassword').css('color', 'red');
            $scope.isValidNewPassword = false;
        } else {
            if ($scope.new_password == '' && $scope.confirm_password == '')
                $scope.isValidNewPassword = false;
            else
                $scope.isValidNewPassword = true;
            $('.lblConfirmPassword').css('color', '#b0b0b0');
        }
        $scope.updateIsChangePassword();
    };

    $scope.updateIsChangePassword = function () {
        if ($scope.isValidNewPassword && $scope.old_password != '')
            $scope.isChangePassword = 1;
        else
            $scope.isChangePassword = 0;
    };

    $scope.alertToaster = function () {
        if ($scope.message_content != '') {
            $('#block-message').show(1000);
            setTimeout(function () {
                $('#block-message').hide(1000);
            }, 2000);
        }
    };

    $scope.checkChangePasswordCommit = function () {
        if ((($scope.old_password == '' || $scope.old_password == undefined)
            && ($scope.new_password == '' || $scope.new_password == undefined)
            && ($scope.confirm_password == '' || $scope.confirm_password == undefined))
            || $scope.isChangePassword == 1)
            return true;
        else
            return false;
    };

}]);

function initAffix() {

    var fixed = false;
    var absolute = false;
    $('.affix-sidebar').height($(window).height());
    $('.affix-main').css('min-height', $(window).height());

    function checkAffix() {

        var underHeader = $(window).scrollTop() > ($('.navbar-inverse').outerHeight() + $('#library_controller').outerHeight() + 15 - $('#global_navbar').height() + $('.followers').outerHeight() + $('.following').outerHeight());
        var underFooter = $(window).scrollTop() + $(window).height() > $('#footer').offset().top - $('#global_navbar').height();

        if (!underHeader && !fixed) { //top
            $('.chef-data').removeClass('active');
            $('.affix-sidebar').removeClass('cb-affix');
            $('.affix-sidebar').removeClass('cb-affix-bottom');
            $('.affix-sidebar').height($(window).height() - $('#global_navbar').height());
            $('.affix-sidebar').find('.scrollable-list').height($(window).height() - $('#global_navbar').height());
            $('.affix-main').css('margin-left', 0);
            absolute = false;
        }
        if (!underHeader && fixed) { //top
            $('.chef-data').removeClass('active');
            $('.affix-sidebar').removeClass('cb-affix');
            $('.affix-sidebar').removeClass('cb-affix-bottom');
            $('.affix-sidebar').height($(window).height() - $('#global_navbar').height());
            $('.affix-sidebar').find('.scrollable-list').height($(window).height() - 100 - $('#global_navbar').height());
            $('.affix-main').css('margin-left', 0);
            fixed = false;
            absolute = false;
        }
        if (underHeader && !underFooter && !fixed) { //fixed
            fixed = true;
            absolute = false;
            $('.chef-data').addClass('active');
            $('.affix-sidebar').addClass('cb-affix');
            $('.affix-sidebar').removeClass('cb-affix-bottom');
            $('.affix-main').css('margin-left', $('.affix-sidebar').css('width'));
            $('.affix-sidebar').height($(window).height() - $('#global_navbar').height());
            $('.affix-sidebar').find('.scrollable-list').height($(window).height() - 100 - $('#global_navbar').height());
        }
        if (underHeader && underFooter) { //bottom
            fixed = false;
            absolute = true;
            $('.affix-sidebar').removeClass('cb-affix');
            $('.affix-sidebar').addClass('cb-affix-bottom');
            $('.affix-sidebar').height($(window).height());
            $('.affix-sidebar').find('.scrollable-list').height($(window).height() - $('.chef-data').height());
            $('.affix-main').css('margin-left', $('.affix-sidebar').css('width'));
        }
    }

    $(window).scroll(function () {
        checkAffix();
    }).resize(function () {
        $('.affix-sidebar').height($(window).height() - $('#global_navbar').height());
        $('.affix-main').css('min-height', $(window).height() - $('#global_navbar').height());
        if (fixed || absolute) {
            $('.chef-data').css('width', $('.affix-sidebar').width())
            $('.affix-main').css('margin-left', $('.affix-sidebar').css('width'));
            $('.affix-sidebar').find('.scrollable-list').height($(window).height() - 100 - $('#global_navbar').height());
        }

    });

    checkAffix();
}
function showDeleteChefModal() {
    var modal = $('#delete_chef_modal');
    modal.modal('show');
    var modal2 = $('#edit_profile_modal');
    modal2.modal('hide');
}


$(document).ready(function () {

    $('#upload_avatar_image_button').click(function () {
        $('#upload_avatar_image_input').click();
    });

    $('#upload_avatar_image_input').change(function (evt) {
        var scope = angular.element(document.getElementById('library_controller')).scope();
        scope.uploadAvatarImage(evt.target.files);
    });

    $('#upload_cover_image_button').click(function () {
        $('#upload_cover_image_input').click();
    });

    $('#upload_cover_image_input').change(function (evt) {
        var scope = angular.element(document.getElementById('library_controller')).scope();
        scope.uploadCoverImage(evt.target.files);
    });

    $('#upload_restaurant_image_button').click(function () {
        $('#upload_restaurant_image_input').click();
    });

    $('#upload_restaurant_image_input').change(function (evt) {
        var scope = angular.element(document.getElementById('library_controller')).scope();
        scope.uploadRestaurantImage(evt.target.files);
    });
    initAffix();
});