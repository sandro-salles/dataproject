'use strict';

describe('Controller: MailInboxCtrl', function () {

  // load the controller's module
  beforeEach(module('minovateApp'));

  var MailInboxCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MailInboxCtrl = $controller('MailInboxCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
