'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:PagesLoginCtrl
 * @description
 * # PagesLoginCtrl
 * Controller of the CONTACTPRO
 */
app
    .controller('LoginCtrl', ['$rootScope', '$window', '$location', '$scope', '$state', '$http', 'jwtHelper', 'AuthService', function($rootScope, $window, $location, $scope, $state, $http, jwtHelper, AuthService) {
        $scope.credentials = {};
        $scope.error = null;

        $scope.onSuccess = function(response) {
            AuthService.SetCredentials(response.data);

            var origin = $location.search().origin;

            if (typeof origin !== 'undefined' && origin) {
                $window.location = '#' + decodeURIComponent(origin);
            } else {
                $window.location = '#/app/dashboard/';
            }
        };

        $scope.onError = function(response) {
            if (response.status == 400) {
                $scope.error = response.data.non_field_errors[0];
            }
        };

        $scope.login = function() {
            $scope.credentials.token = AuthService.Login($scope.credentials.username, $scope.credentials.password, $scope.onSuccess, $scope.onError);
        };
    }]);
