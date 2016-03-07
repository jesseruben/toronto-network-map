'use strict';


angular.module('app', [
    'ngAnimate',
    'ngAria',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngSanitize',
    'ngTouch',
    'ngStorage',
    'ui.router',
    'ui.bootstrap',
    'ui.utils',
    'ui.load',
    'ui.jq',
    'oc.lazyLoad',
    'pascalprecht.translate',
    'speedtest',
    'report',
    'Authentication',
    'angular-logger',
    'loginModal',
    'toaster',
    'GeoLocation',
    'uiGmapgoogle-maps',
    'angucomplete-alt',
    'ui.slider',
    'ngPersian',
    'angularjs-dropdown-multiselect'
]);


angular
      .module('app')
      .run(run);

  run.$inject = ['$http'];

  /**
  * @name run
  * @desc Update xsrf $http headers to align with Django's defaults
  */
  function run($http) {

      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
  }
