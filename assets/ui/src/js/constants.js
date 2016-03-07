(function () {
    'use strict';

    var config_data = {
        'PATH': {
            'BASE_TEMPLATE_URL': 'static/tpl/'
        },
        'AUTH_EVENTS': {
              loginSuccess: 'auth-login-success',
              loginFailed: 'auth-login-failed',
              logoutSuccess: 'auth-logout-success',
              sessionTimeout: 'auth-session-timeout',
              notAuthenticated: 'auth-not-authenticated',
              notAuthorized: 'auth-not-authorized'
        },'USER_ROLES': {
              all: '*',
              admin: 'loggedin',
              editor: 'editor',
              guest: 'guest'
        }
    };

    angular.forEach(config_data, function(key, value) {
        angular.module('app').constant(value, key);
    });

})();
