(function () {
  'use strict';

/**
 * @ngdoc overview
 * @name ndtApp
 * @description
 * # ndtApp
 *
 * Main module of the application.
 */
angular
  .module('ndtApp', [
    'ndtApp.config',
    'ndtApp.constants',
    'ndtApp.routes',
    'ngAnimate',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ui.bootstrap',
    'pascalprecht.translate',
    'cgNotify',
    'uiGmapgoogle-maps',
    'angular-logger',
    'ndtApp.authentication',
    'ndtApp.speedtest',
    'ndtApp.reports',
    'ndtApp.static',
    'ndtApp.contact',
    'ndtApp.ndt',
    'ngAria',
    'ngMaterial',
    'ui.slider',
    'ngMessages'
  ]);

  angular
      .module('ndtApp.config', []);

  angular
      .module('ndtApp.constants', []);

  angular
      .module('ndtApp.routes', ['ngRoute']);

  angular
      .module('ndtApp')
      .run(run);

  run.$inject = ['$http', '$rootScope', '$translate'];

  /**
  * @name run
  * @desc Update xsrf $http headers to align with Django's defaults
  */
  function run($http, $rootScope, $translate) {
     /**
      *  Listening to route change and changing the page title
      */
      $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
          if (current.$$route.title){
              $translate(current.$$route.title).then(titleTranslateSuccess, titleTranslateFailure);
          }
          // It's advised not to put function declaration inside conditional clauses
          function titleTranslateSuccess (translatedString){
              $rootScope.title = translatedString;
          }

          function titleTranslateFailure(){
              $rootScope.title = current.$$route.title;
          }

      });
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    }
})();

