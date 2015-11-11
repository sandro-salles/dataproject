'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:PagesChatCtrl
 * @description
 * # PagesChatCtrl
 * Controller of the CONTACTPRO
 */
app
  .controller('ChatCtrl', function ($scope, $resource) {
    $scope.inbox = $resource('scripts/jsons/chats.json').query();

    $scope.archive = function(index) {
      $scope.inbox.splice(index, 1);
    };
  });
