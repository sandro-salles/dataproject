'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:vectorMap
 * @description
 * # vectorMap
 */
app
  .directive('vectorMap', function () {
    return {
      restrict: 'AE',
      scope: {
        options: '='
      },
      link: function postLink(scope, element) {
        var options = scope.options;
        element.vectorMap(options);
      }
    };
  });
