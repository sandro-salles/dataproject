'use strict';

/**
 * @ngdoc function
 * @name DATAPROJECT.controller:PagesChatCtrl
 * @description
 * # PagesChatCtrl
 * Controller of the DATAPROJECT
 */
app
  .controller('ChatCtrl', function ($scope, $resource) {
    $scope.inbox = $resource('scripts/jsons/chats.json').query();

    $scope.archive = function(index) {
      $scope.inbox.splice(index, 1);
    };
  });
