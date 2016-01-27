'use strict';

app

  .controller('mtSwitchCtrl', function($scope, $timeout, $mdBottomSheet) {

    $scope.page = {
      title: 'Switch',
      subtitle: ''
    };

    $scope.data = {
      cb1: true,
      cb4: true,
      cb5: false
    };
    $scope.onChange = function(cbState) {
      $scope.message = "The switch is now: " + cbState;
    };

  });




