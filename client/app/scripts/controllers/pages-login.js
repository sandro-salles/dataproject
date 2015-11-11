'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:PagesLoginCtrl
 * @description
 * # PagesLoginCtrl
 * Controller of the CONTACTPRO
 */
app
  .controller('LoginCtrl', function ($scope, $state) {
    $scope.login = function() {
      $state.go('app.dashboard');
    };
  });
