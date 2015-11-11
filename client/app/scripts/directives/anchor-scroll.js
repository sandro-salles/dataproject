'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:anchorScroll
 * @description
 * # anchorScroll
 */
app
  .directive('anchorScroll', ['$location', '$anchorScroll', function($location, $anchorScroll) {
    return {
      restrict: 'AC',
      link: function(scope, el, attr) {
        el.on('click', function(e) {
          $location.hash(attr.anchorScroll);
          $anchorScroll();
        });
      }
    };
  }]);
