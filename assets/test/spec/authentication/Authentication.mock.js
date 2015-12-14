/*
 * Mocking authentication service for controllers
 * */
angular.module('AuthenticationMock', [])
    .provider('Authentication', function() {
        this.$get = function() {
            return {
                login: function() {return true;},
                isAuthenticated : function () { return true; },
                logout: function() {}
            };
        };
    });