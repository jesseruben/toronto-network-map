'use strict';

/**
 * Config for the router
 */
angular.module('app')
  .run(
    ['$rootScope', '$state', '$stateParams', 'AUTH_EVENTS', 'Authentication', 'loginModal',
      function ($rootScope, $state, $stateParams, AUTH_EVENTS, Authentication, loginModal) {
          $rootScope.$state = $state;
          $rootScope.$stateParams = $stateParams;

          /*Checking application state changes for access control for authorization*/
          $rootScope.$on('$stateChangeStart', function (event, toState, toParams) {
              var authorizedRoles = toState.data.authorizedRoles;
              if (!Authentication.isAuthorized(authorizedRoles)) {
                  event.preventDefault();
                  Authentication.launchModal()
                        .then(function () {
                          console.log('route config success login');
                          return $state.go(toState.name, toParams);
                        })
                        .catch(function () {
                          console.log('route config unsuccess login');
                          return $state.go('app.dashboard-v1');
                        });
                  if (Authentication.isAuthenticated()) {
                      // user is not allowed
                      $rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
                  } else {
                      // user is not logged in
                      $rootScope.$broadcast(AUTH_EVENTS.notAuthenticated);
                  }
              }
          }); //End of rootScope.$On
      }
    ]
  )
  .config(
    [          '$stateProvider', '$urlRouterProvider', 'JQ_CONFIG', 'MODULE_CONFIG', 'USER_ROLES',
      function ($stateProvider,   $urlRouterProvider, JQ_CONFIG, MODULE_CONFIG, USER_ROLES) {
          //Getting language code from localstorage
          var lang='fa'; // we don't have access to the translate service here
          if(typeof(Storage) !== "undefined" && localStorage.getItem("NG_TRANSLATE_LANG_KEY")) {
            lang = localStorage.getItem("NG_TRANSLATE_LANG_KEY");
          }
          var layout = "static/src/tpl/layout.html";
          if(lang == 'fa'){
            layout = "static/src/tpl/layoutrtl.html";
          }
          $urlRouterProvider.otherwise('/app/home');
          $stateProvider
              .state('app', {
                  abstract: true,
                  url: '/app',
                  templateUrl: layout
              })
              .state('app.home', {
                  url: '/home',
                  templateUrl: lang=='fa' ? 'static/src/tpl/homertl.html' : 'static/src/tpl/home.html',
                  resolve: load(['static/src/js/controllers/speedtest.js', 'static/src/js/controllers/report.js']),
                  data: {
                        authorizedRoles: [USER_ROLES.all]
                  }
              })
              .state('app.setpassword', {
                  url: '/setpassword/:guid',
                  templateUrl: 'static/src/tpl/set-password.html',
                  controllerAs: 'vm',
                  controller: 'SetPasswordController',
                  resolve: load(['static/src/js/controllers/setpassword.js']),
                  data: {
                        authorizedRoles: [USER_ROLES.all]
                  }
              })
              .state('app.updatepassword', {
                  url: '/updatepassword',
                  templateUrl: 'static/src/tpl/account.html',
                  controllerAs: 'vm',
                  controller: 'AccountController',
                  resolve: load(['static/src/js/controllers/account.js']),
                  data: {
                        authorizedRoles: [USER_ROLES.loggedin]
                  }
              })
              .state('app.about', {
                  url: '/about',
                  templateUrl: lang=='fa' ? 'static/src/tpl/aboutrtl.html' : 'static/src/tpl/about.html',
                  controllerAs: 'vm',
                  controller: 'FaqController',
                  resolve: load(['static/src/js/controllers/faq.js']),
                  data: {
                        authorizedRoles: [USER_ROLES.all]
                  }
               })
              .state('app.isps', {
                  url: '/isps',
                  templateUrl: 'static/src/tpl/isp-list.html',
                  controllerAs: 'vm',
                  controller: 'IspListController',
                  resolve: load(['static/src/js/controllers/ispList.js']),
                  data: {
                        authorizedRoles: [USER_ROLES.all]
                  }
              })
              .state('app.isp', {
                  url: '/isp/{id:int}/{name}',
                  templateUrl: 'static/src/tpl/isp-detail.html',
                  controllerAs: 'vm',
                  controller: 'IspDetailController',
                  resolve: load(['static/src/js/controllers/ispDetail.js']),
                  data: {
                        authorizedRoles: [USER_ROLES.all]
                  }
              })
              .state('app.contact', {
                  url: '/contact',
                  templateUrl: 'static/src/tpl/contact.html',
                  controllerAs: 'vm',
                  controller: 'ContactController',
                  resolve: load(['static/src/js/controllers/contact.js']),
                  data: {
                        authorizedRoles: [USER_ROLES.all]
                  }
              })
              .state('app.map', {
                  url: '/map',
                  templateUrl: lang=='fa' ? 'static/src/tpl/maprtl.html' : 'static/src/tpl/map.html',
                  controllerAs: 'vm',
                  controller: 'MapController',
                  resolve: load(['static/src/js/controllers/map.js']),
                  data: {
                        authorizedRoles: [USER_ROLES.all]
                  }
              });

          function load(srcs, callback) {
            return {
                deps: ['$ocLazyLoad', '$q',
                  function( $ocLazyLoad, $q ){
                    var deferred = $q.defer();
                    var promise  = false;
                    srcs = angular.isArray(srcs) ? srcs : srcs.split(/\s+/);
                    if(!promise){
                      promise = deferred.promise;
                    }
                    angular.forEach(srcs, function(src) {
                      promise = promise.then( function(){
                        if(JQ_CONFIG[src]){
                          return $ocLazyLoad.load(JQ_CONFIG[src]);
                        }
                        angular.forEach(MODULE_CONFIG, function(module) {
                          if( module.name == src){
                            name = module.name;
                          }else{
                            name = src;
                          }
                        });
                        return $ocLazyLoad.load(name);
                      } );
                    });
                    deferred.resolve();
                    return callback ? promise.then(function(){ return callback(); }) : promise;
                }]
            }
          }


      }
    ]
  );
