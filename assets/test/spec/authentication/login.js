describe('login', function() {
  var module;

  beforeEach(function() {
    module =  angular.module('ndtApp.authentication');
  });

  it("should be registered", function() {
    expect(module).not.toBe(null);
    expect(module).not.toBe(undefined);
  });
});