'use strict';

describe('Controller: OffcanvaslayoutCtrl', function () {

  // load the controller's module
  beforeEach(module('minovateApp'));

  var OffcanvaslayoutCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    OffcanvaslayoutCtrl = $controller('OffcanvaslayoutCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
