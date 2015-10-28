'use strict';

/**
 * @ngdoc function
 * @name DATAPROJECT.controller:NavCtrl
 * @description
 * # NavCtrl
 * Controller of the DATAPROJECT
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
