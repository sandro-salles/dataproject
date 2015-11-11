'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:NavCtrl
 * @description
 * # NavCtrl
 * Controller of the CONTACTPRO
 */
app
  .controller('NavCtrl', function ($scope) {
    $scope.oneAtATime = false;

    $scope.status = {
      isFirstOpen: true,
      isSecondOpen: true,
      isThirdOpen: true
    };

  });
