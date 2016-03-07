/**
* SetPasswordController
* @namespace app.controllers
*/
(function () {
  'use static';

  angular
    .module('app')
    .controller('SetPasswordController', SetPasswordController);

  SetPasswordController.$inject = ['$stateParams', 'Authentication', '$filter'];

  /**
  * @namespace SetPasswordController
  */
  function SetPasswordController($stateParams, Authentication, $filter) {
    var vm = this;

    vm.setPassword = setPassword;
    vm.getError = getError;

   /**
    * @name setPassword
    * @desc Setting a new password
    * @memberOf ndtApp.authentication.controllers.SetPasswordController
    */
    function setPassword(){
       var guid = $stateParams.guid;
       Authentication.setPassword(guid, vm.new_password, vm.confirm_password);
    }

    /**
    * @name getError
    * @desc Getting error for the form element
    * @memberOf ndtApp.authentication.controllers.setPasswordController
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