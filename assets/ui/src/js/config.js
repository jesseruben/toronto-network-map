// config

var app =
    angular.module('app')
        .config(
        [        '$controllerProvider', '$compileProvider', '$filterProvider', '$provide',
            function ($controllerProvider,   $compileProvider,   $filterProvider,   $provide) {

                // lazy controller, directive and service
                app.controller = $controllerProvider.register;
                app.directive  = $compileProvider.directive;
                app.filter     = $filterProvider.register;
                app.factory    = $provide.factory;
                app.service    = $provide.service;
                app.constant   = $provide.constant;
                app.value      = $provide.value;
            }
        ])
        .config(['$translateProvider', function($translateProvider){
            // Register a loader for the static files
            // So, the module will search missing translation tables under the specified urls.
            // Those urls are [prefix][langKey][suffix].
            $translateProvider.useStaticFilesLoader({
                prefix: 'static/src/l10n/',
                suffix: '.json'
            });
            // Tell the module what language to use by default
            $translateProvider.preferredLanguage('fa');
            // Tell the module to store the language in the local storage
            $translateProvider.useLocalStorage();
        }
        ])
        .config(function ($httpProvider) {
            $httpProvider.interceptors.push([
                '$injector',
                function ($injector) {
                    return $injector.get('AuthInterceptor');
                }
            ]);
        })
        .factory('AuthInterceptor', function ($rootScope, $q, AUTH_EVENTS) {
            return {
                responseError: function (response) {
                    $rootScope.$broadcast({
                        401: AUTH_EVENTS.notAuthenticated,
                        403: AUTH_EVENTS.notAuthorized,
                        419: AUTH_EVENTS.sessionTimeout,
                        440: AUTH_EVENTS.sessionTimeout
                    }[response.status], response);
                    return $q.reject(response);
                }
            };
        });
