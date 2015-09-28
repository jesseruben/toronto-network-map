(function () {
  'use strict';

  angular
    .module('ndtApp.routes')
    .config(config);

  config.$inject = ['$routeProvider', '$logProvider', 'PATH'];

  function config($routeProvider, $logProvider, PATH) {
    $logProvider.debugEnabled(true);

    $routeProvider.when('/', {
        templateUrl: PATH.BASE_TEMPLATE_URL + 'static/main.html',
        controller: 'StaticPageController',
        controllerAs: 'vm'
      }).when('/about', {
        templateUrl: PATH.BASE_TEMPLATE_URL + 'static/about.html',
        controller: 'StaticPageController',
        controllerAs: 'vm'
      }).when('/contact', {
        templateUrl: PATH.BASE_TEMPLATE_URL + 'contact/contact.html',
        controller: 'ContactController',
        controllerAs: 'vm'
      }).when('/speedtest', {
        templateUrl: PATH.BASE_TEMPLATE_URL + 'speedtest/speedtest.html',
        controller: 'SpeedtestController',
        controllerAs: 'vm'
      }).when('/settings/:username', {
        controller: 'AccountController',
        controllerAs: 'vm',
        title: 'SETTINGS',
        templateUrl: PATH.BASE_TEMPLATE_URL + 'authentication/account.html'
       }).when('/register', {
        controller: 'RegisterController',
        controllerAs: 'vm',
        title: 'REGISTER',
        templateUrl: PATH.BASE_TEMPLATE_URL + 'authentication/register.html'
      }).when('/login', {
        controller: 'LoginController',
        controllerAs: 'vm',
        title: 'LOGIN',
        templateUrl: PATH.BASE_TEMPLATE_URL + 'authentication/login.html'
      }).when('/error-404', {
        controller: 'StaticPageController',
        controllerAs: 'vm',
        title: 'ERROR_404',
        templateUrl: PATH.BASE_TEMPLATE_URL + 'static/404.html'
      }).when('/forgotpassword', {
        controller: 'ForgotPasswordController',
        controllerAs: 'vm',
        title: 'FORGOTPASSWORD',
        templateUrl: PATH.BASE_TEMPLATE_URL + 'authentication/forgot-password.html'
      }).when('/setpassword/:guid', {
        controller: 'SetPasswordController',
        controllerAs: 'vm',
        title: 'SET_YOUR_PASS',
        templateUrl: PATH.BASE_TEMPLATE_URL + 'authentication/set-password.html'
      }).otherwise({
        redirectTo: '/error-404'
      });
    }
})();