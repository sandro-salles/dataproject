'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:todoFocus
 * @description
 * # todoFocus
 */
app
  .directive('todoFocus', function ($timeout) {
    return {
      restrict: 'A',
      link: function postLink(scope, element, attrs) {
        scope.$watch(attrs.todoFocus, function (newVal) {
          if (newVal) {
            $timeout(function () {
              element[0].focus();
            }, 0, false);
          }
        });
      }
    };
  });
