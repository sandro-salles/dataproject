'use strict';

app

  .controller('mtSwipeCtrl', function($scope, $timeout, $mdBottomSheet) {

    $scope.page = {
      title: 'Swipe',
      subtitle: ''
    };

    $scope.onSwipeLeft = function(ev) {
      alert('You swiped left!!');
    };
    $scope.onSwipeRight = function(ev) {
      alert('You swiped right!!');
    };

  });




