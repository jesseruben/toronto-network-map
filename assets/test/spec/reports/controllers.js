describe('report', function() {
    var module;

    beforeEach(function () {
        module = angular.module('ndtApp.reports');
    });

    it("should be registered", function () {
        expect(module).not.toBe(null);
        expect(module).not.toBe(undefined);
    })
});