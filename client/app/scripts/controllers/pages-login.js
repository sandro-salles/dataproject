'use strict';

/**
 * @ngdoc function
 * @name DATAPROJECT.controller:PagesLoginCtrl
 * @description
 * # PagesLoginCtrl
 * Controller of the DATAPROJECT
 */
app
  .controller('LoginCtrl', function ($scope, $state) {
    $scope.login = function() {
      $state.go('app.dashboard');
    };
  });
