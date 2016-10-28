/**
 * Created by apium on 16/03/2016.
 */
app.controller("EnterpriseCtrl", function($scope, $http) {
    $scope.onLoad = function() {
        $scope.getCountryCode();
    };

    $scope.getCountryCode = function() {
        $http.get("https://restcountries.eu/rest/v1/all").then(function(response) {
            $scope.countryCode = $scope.decorateCountryCode(response.data);
        });
    };

    $scope.decorateCountryCode = function(countryCodeList) {
        return countryCodeList.map(function(e) {
            if (e.callingCodes)
                return e.name + ' (+' + e.callingCodes[0] + ')';
        });
    };
});

