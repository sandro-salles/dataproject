'use strict';

app

  .controller('mtButtonsCtrl', function($scope, $timeout, $mdBottomSheet) {

    $scope.page = {
      title: 'Buttons',
      subtitle: ''
    };

    $scope.title1 = 'Button';
    $scope.title4 = 'Warn';
    $scope.isDisabled = true;
    $scope.googleUrl = 'http://google.com';

  });




