'use strict';

/**
 * @ngdoc directive
 * @name DATAPROJECT.directive:tileControlFullscreen
 * @description
 * # tileControlFullscreen
 */
app
  .directive('tileControlFullscreen', function () {
    return {
      restrict: 'A',
      link: function postLink(scope, element) {
        var dropdown = element.parents('.dropdown');

        element.on('click', function(){
          dropdown.trigger('click');
        });

      }
    };
  });
