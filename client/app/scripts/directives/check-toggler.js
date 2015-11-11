'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:checkToggler
 * @description
 * # checkToggler
 */
app
  .directive('checkToggler', function () {
    return {
      restrict: 'E',
      link: function postLink(scope, element) {
        element.on('click', function(){

          if (element.hasClass('checked')) {
            element.removeClass('checked');
          } else {
            element.addClass('checked');
          }

        });
      }
    };
  });
