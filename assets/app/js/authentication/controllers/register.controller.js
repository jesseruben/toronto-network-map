/**
 * Register controller
 * With a service and interface in place, we need a controller to hook the two together
 * template is in top template folder and service is in the services folder
 * @namespace ndtApp.authentication.controllers
 */

(function () {
  'use strict';

  angular
    .module('ndtApp.authentication.controllers')
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location','$filter', 'Authentication', '$log'];

  /**
   * @namespace RegisterController
   */
  function RegisterController($location, $filter, Authentication, $log) {
    var vm = this;
    var logger = $log.getInstance('RegisterController');

    /*
    vm allows the template we just created to access the register method we define later in the controller
     */
    vm.register = register;
    vm.getError = getError;

    //Regular expression for password
    vm.matchPattern = new RegExp("^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*[\d\W]).*$")
    /*
        (/^
        (?=.*\d)                //should contain at least one digit
        (?=.*[a-z])             //should contain at least one lower case
        (?=.*[A-Z])             //should contain at least one upper case
        [a-zA-Z0-9]{8,}         //should contain at least 8 and at most 24 from the mentioned characters
        $/)
     */


    activate();

    /**
     * @name activate
     * @desc Actions to be performed when this controller is instantiated
     * @memberOf ndtApp.authentication.controllers.RegisterController
     */
    function activate() {
      logger.info("Activate is called.");
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        $location.url('/');
      }
    }

    /**
     * @name register
     * @desc Register a new user
     * @memberOf ndtApp.authentication.controllers.RegisterController
     */
    function register() {
      logger.info('Register function is called by submit button');
      // Call the authentication method in the service we just made
      Authentication.register(vm.email, vm.password, vm.confirm_password, vm.username);
    }

      /**
       * @name getError
       * @desc Getting error for the form element
       * @memberOf ndtApp.authentication.controllers.RegisterController
       */
      function getError (error, min, max){
          if (angular.isDefined(error)){
              if (error.required){
                  return $filter('translate')('ERROR_REQUIRED');
              } else if (error.email){
                  return $filter('translate')('ERROR_EMAIL');
              } else if (error.minlength){
                  return $filter('translate')('ERROR_SHORT')+ min;
              } else if (error.maxlength){
                  return $filter('translate')('ERROR_LONG')+ max;
              } else if (error.pattern){
                  return $filter('translate')('ERROR_PASSWORD_REGEX');
              } else if (error.pwmatch){
                  return $filter('translate')('ERROR_PASSWORD_MATCH');
              } else if (error.alphanumeric){
                  return $filter('translate')('ERROR_ALPHA_NUMERIC');
              }
          }
      }
  }
})();