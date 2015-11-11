'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:TileControlClose
 * @description
 * # TileControlClose
 */
app
  .directive('tileControlClose', function () {
    return {
      restrict: 'A',
      link: function postLink(scope, element) {
        var tile = element.parents('.tile');

        element.on('click', function() {
          tile.addClass('closed').fadeOut();
        });
      }
    };
  });
