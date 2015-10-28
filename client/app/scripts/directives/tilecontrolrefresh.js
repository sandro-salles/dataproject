'use strict';

/**
 * @ngdoc directive
 * @name DATAPROJECT.directive:tileControlRefresh
 * @description
 * # tileControlRefresh
 */
app
  .directive('tileControlRefresh', function () {
    return {
      restrict: 'A',
      link: function postLink(scope, element) {
        var tile = element.parents('.tile');
        var dropdown = element.parents('.dropdown');

        element.on('click', function(){
          tile.addClass('refreshing');
          dropdown.trigger('click');
        });
      }
    };
  });
