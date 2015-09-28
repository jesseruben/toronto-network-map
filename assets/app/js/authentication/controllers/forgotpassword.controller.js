/**
* ForgotPasswordController
* @namespace ndtApp.authentication.controllers
*/
(function () {
  'use static';

  angular
    .module('ndtApp')
    .controller('ForgotPasswordController', ForgotPasswordController);

  ForgotPasswordController.$inject = ['Authentication', '$filter'];

  /**
  * @namespace ForgotPasswordController
  */
  function ForgotPasswordController(Authentication, $filter) {
    var vm = this;

    vm.sendForgotPasswordEmail = sendForgotPasswordEmail;
    vm.getError = getError;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated, nothing special
    * @memberOf ndtApp.authentication.controllers.ForgotPasswordController
    */
    function activate() {
        vm.emailSentSuccessfully = false;
    }

    /**
    * @name sendForgotPasswordEmail
    * @desc Sending Forgot Password Email
    * @memberOf ndtApp.authentication.controllers.ForgotPasswordController
    */
    function sendForgotPasswordEmail()
    {
        Authentication.sendForgotPasswordEmail(vm.email);
    }

    /**
    * @name getError
    * @desc Getting error for the form element
    * @memberOf ndtApp.authentication.controllers.ForgotPasswordController
    */
    function getError (error, min, max){
      if (angular.isDefined(error)){
          if (error.required){
              return $filter('translate')('ERROR_REQUIRED');
          } else if (error.email){
              return $filter('translate')('ERROR_EMAIL');
          }
      } else return;
    }

  }
})();