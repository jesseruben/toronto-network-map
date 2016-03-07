// LoginModalCtrl.js
/**
 * LoginController
 * @namespace ndtApp.authentication.controllers
 */
(function () {
    'use static';

    app.controller('LoginModalCtrl', LoginModalCtrl);

    LoginModalCtrl.$inject = ['Authentication', '$log', '$scope', '$rootScope','$filter','tab'];

    /**
     * @namespace LoginModalCtrl
     */
    function LoginModalCtrl(Authentication,  $log,  $scope, $rootScope, $filter, tab) {
        var logger = $log.getInstance('Login Modal Controller');
        vm = this;
        vm.pages = ['login', 'signup', 'forgotpassword'];
        vm.getCurrentPage = getCurrentPage;
        vm.setCurrentPage = setCurrentPage;
        vm.login = login;
        vm.forgotPassword = forgotPassword;
        vm.register = register;
        vm.cancel = $scope.$dismiss;
        vm.getError = getError;

        activate();


        function activate() {
            if(tab){
                vm.page = tab;
            } else {
                vm.page = 0; //show login by default
            }
        }

        function getCurrentPage (){
            return vm.pages[vm.page];
        }


        function setCurrentPage (page){
            vm.page = page;
        }


        function login (email, password) {
            logger.info('Authentication login service is called inside the modal controller');
            Authentication.login(vm.email, vm.password).then(loginSuccess, loginError);


            function loginSuccess (user) {
                // passing user the data to the service (Authentication) who called this controller
                $scope.$close(user);
            }

            function loginError(response){
                vm.loginError = $filter('translate')('errors.' + response.message);
            }
        };

        function register() {
            logger.info('Authentication register service is called inside the modal controller');
            Authentication.register(vm.email, vm.password, vm.confirm_password, vm.username)
                .then(registerSuccess, registerError);


            function registerSuccess (user) {
                // passing user the data to the service (Authentication) who called this controller
                logger.log('registerSuccess was called');
                $scope.$close(user);
            }

            function registerError(response){
                logger.error('registerError was called '+response.message);
                vm.registerError = $filter('translate')('errors.' + response.message);
            }
        };

        function forgotPassword()
        {
            logger.info('forgot password function is called');
            Authentication.sendForgotPasswordEmail(vm.email).then(function(){
               vm.isCollapsed = false;
            });
        }

         function getError (error, min, max){
          if (angular.isDefined(error)){
              if (error.required){
                  return $filter('translate')('errors.ERROR_REQUIRED');
              } else if (error.email){
                  return $filter('translate')('errors.ERROR_EMAIL');
              } else if (error.minlength){
                  return $filter('translate')('errors.ERROR_SHORT')+ min;
              } else if (error.maxlength){
                  return $filter('translate')('errors.ERROR_LONG')+ max;
              } else if (error.pattern){
                  return $filter('translate')('errors.ERROR_PASSWORD_REGEX');
              } else if (error.pwmatch){
                  return $filter('translate')('errors.ERROR_PASSWORD_MATCH');
              } else if (error.alphanumeric){
                  return $filter('translate')('errors.ERROR_ALPHA_NUMERIC');
              }
          }
        }

    }
})();
