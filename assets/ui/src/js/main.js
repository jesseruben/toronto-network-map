'use strict';

/* Controllers */

angular.module('app')
    .controller('AppCtrl', ['$scope', '$translate', '$localStorage', '$window', 'USER_ROLES', 'Authentication','AUTH_EVENTS', 'toaster',
        function($scope,   $translate,   $localStorage,   $window, USER_ROLES, Authentication, AUTH_EVENTS, toaster ) {

            // add 'ie' classes to html
            var isIE = !!navigator.userAgent.match(/MSIE/i);
            isIE && angular.element($window.document.body).addClass('ie');
            isSmartDevice( $window ) && angular.element($window.document.body).addClass('smart');

            // config
            $scope.app = {
                name: 'آیسپی فای',
                version: ' Alpha release',
                // for chart colors
                color: {
                    primary: '#7266ba',
                    info:    '#23b7e5',
                    success: '#27c24c',
                    warning: '#fad733',
                    danger:  '#f05050',
                    light:   '#e8eff0',
                    dark:    '#3a3f51',
                    black:   '#1c2b36',
                    primary_light: '#e0dcef',
                    info_light: '#d1f0fa'
                },
                settings: {
                    themeID: 1,
                    navbarHeaderColor: 'bg-black',
                    navbarCollapseColor: 'bg-white-only',
                    asideColor: 'bg-black',
                    headerFixed: true,
                    asideFixed: false,
                    asideFolded: false,
                    asideDock: true,
                    container: false
                }
            };

            /* Instantiating current user, assignment occurs in login and authentication service
             * Assignment cannot be done in child due to shadow property so we have to use a setter function
             * userRoles and isAuthorize will be used in template and not other controllers to avoid testing complication */
            $scope.currentUser = Authentication.getAuthenticatedAccount();
            $scope.userRoles = USER_ROLES;
            $scope.isAuthorized = Authentication.isAuthorized;
            $scope.$on(AUTH_EVENTS.loginSuccess,function(){
                //listening to loginSuccess event and updating current user value, used in header template
                $scope.currentUser= Authentication.getAuthenticatedAccount();
            });

            $scope.logout = function() {
                Authentication.logout().then(logoutSuccess);
                function logoutSuccess(){
                    $scope.currentUser= null;
                }
            };

            /**
             * open login modal
             * @param tab defines which tab should be opened in the modal, 0-> login
             */
            $scope.login = function(tab) {
                Authentication.launchModal(tab)
                    .then(function () {
                    })
                    .catch(function () {
                    });
            };

            /**
             * call the register modal
             * @param tab define which tab should be opened in the modal, 1->register
             */
            $scope.register = function(tab){
                Authentication.launchModal(tab)
                    .then(function () {
                    })
                    .catch(function () {
                    });
            };


            // save settings to local storage
            if ( angular.isDefined($localStorage.settings) ) {
                $scope.app.settings = $localStorage.settings;
            } else {
                $localStorage.settings = $scope.app.settings;
            }
            $scope.$watch('app.settings', function(){
                if( $scope.app.settings.asideDock  &&  $scope.app.settings.asideFixed ){
                    // aside dock and fixed must set the header fixed.
                    $scope.app.settings.headerFixed = true;
                }
                // for box layout, add background image
                $scope.app.settings.container ? angular.element('html').addClass('bg') : angular.element('html').removeClass('bg');
                // save to local storage
                $localStorage.settings = $scope.app.settings;
            }, true);

            // angular translate
            var currentLang = $translate.proposedLanguage();
            if (currentLang =='en'){
               $scope.app.name = 'ISP'
            };
            $scope.lang = { isopen: false };
            $scope.langs = {en:'English', fa:'فارسی'};
            $scope.selectLang = $scope.langs[currentLang] || "English";
            $scope.setLang = function(langKey, $event) {
                // set the current lang
                $scope.selectLang = $scope.langs[langKey];
                // You can change the language during runtime
                $translate.use(langKey);
                $scope.lang.isopen = !$scope.lang.isopen;
            };

            function isSmartDevice( $window )
            {
                // Adapted from http://www.detectmobilebrowsers.com
                var ua = $window['navigator']['userAgent'] || $window['navigator']['vendor'] || $window['opera'];
                // Checks for iOs, Android, Blackberry, Opera Mini, and Windows mobile devices
                // test function look for a matched regex and returns boolean
                return (/iPhone|iPod|iPad|Silk|Android|BlackBerry|Opera Mini|IEMobile/).test(ua);
            }

        }]);
