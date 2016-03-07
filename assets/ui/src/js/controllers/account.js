/**
* AccountController
* @namespace toolApp.authentication.controllers
*/
(function () {
  'use static';

  angular
    .module('app')
    .controller('AccountController', AccountController);

  AccountController.$inject = ['Authentication', '$filter'];

  /**
  * @namespace AccountController
  */
  function AccountController(Authentication, $filter) {
    var vm = this;
    vm.email = '';
    vm.createdAt = '';
    vm.updatedAt = '';
    vm.username = '';
    vm.activeProfile = false;
    vm.activeAnalytics = false;
    vm.activeUserInfo = true;
    vm.activeUpdatePassword = false;
    vm.activeDeactivation = false;

    vm.updatePassword = updatePassword;
    vm.getError = getError;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated, nothing special
    * @memberOf ndtApp.authentication.controllers.AccountController
    */
    function activate() {
      var account = JSON.parse(localStorage.authenticatedAccount);
      vm.createdAt = account.created_at;
      vm.email = account.email;
      vm.updatedAt = account['updatedAt'];
      vm.username = account['username'];

      if (vm.updatedAt == undefined)
         vm.updatedAt = vm.createdAt;

    }

    /**
     * @name updatePassword
     * @desc Update user's password
     * @memberOf ndtApp.authentication.controllers.AccountController
     */
    function updatePassword() {
      // Call the authentication method in the service we just made
      Authentication.updatePassword(vm.user_password, vm.new_password, vm.confirm_password);
    }

    /**
    * @name getError
    * @desc Getting error for the form element
    * @memberOf AccountController
    */
    function getError (error, min, max){
      if (angular.isDefined(error)){
          if (error.required){
              return $filter('translate')('errors.ERROR_REQUIRED');
          } else if (error.minlength){
              return $filter('translate')('errors.ERROR_SHORT')+ min;
          } else if (error.maxlength){
              return $filter('translate')('errors.ERROR_LONG')+ max;
          } else if (error.pattern){
              return $filter('translate')('errors.ERROR_PASSWORD_REGEX');
          } else if (error.pwmatch){
              return $filter('translate')('errors.ERROR_PASSWORD_MATCH');
          }
      }
    }


  }
})();
