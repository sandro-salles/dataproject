'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:PagesForgotPasswordCtrl
 * @description
 * # PagesForgotPasswordCtrl
 * Controller of the CONTACTPRO
 */
app
    .controller('ForgotPasswordCtrl', function($state, $scope, $location) {
        $scope.credentials = {};
        $scope.error = null;

        $scope.onSuccess = function(response) {
            //
        };

        $scope.onError = function(response) {
            if (response.status == 400) {
                $scope.error = response.data.non_field_errors[0];
            }
        };

        $scope.recover = function() {
            $location.path('/core/forgotpass/success');

        };
    })
    .controller('ForgotPasswordSuccessCtrl', function($state, $scope) {
        
    });
