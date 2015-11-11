'use strict';

/**
 * @ngdoc directive
 * @name CONTACTPRO.directive:nativeTab
 * @description
 * # nativeTab
 */
app
  .directive('nativeTab', function () {
    return {
      restrict: 'A',
      link: function( scope , element , attributes ){
        var $element = angular.element(element);
        $element.on('click', function(e) {
          e.preventDefault();
          $element.tab('show');
        });
      }
    };
  });
