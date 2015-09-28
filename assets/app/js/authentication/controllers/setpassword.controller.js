/**
* SetPasswordController
* @namespace ndtApp.authentication.controllers
*/
(function () {
  'use static';

  angular
    .module('ndtApp')
    .controller('SetPasswordController', SetPasswordController);

  SetPasswordController.$inject = ['$routeParams', 'Authentication', '$filter'];

  /**
  * @namespace SetPasswordController
  */
  function SetPasswordController($routeParams, Authentication, $filter) {
    var vm = this;

    vm.setPassword = setPassword;
    vm.getError = getError;

   /**
    * @name setPassword
    * @desc Setting a new password
    * @memberOf ndtApp.authentication.controllers.SetPasswordController
    */
    function setPassword(){
       var guid = $routeParams.guid;
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
              return $filter('translate')('ERROR_REQUIRED');
          } else if (error.minlength){
              return $filter('translate')('ERROR_SHORT')+ min;
          } else if (error.maxlength){
              return $filter('translate')('ERROR_LONG')+ max;
          } else if (error.pattern){
              return $filter('translate')('ERROR_PASSWORD_REGEX');
          } else if (error.pwmatch){
              return $filter('translate')('ERROR_PASSWORD_MATCH');
          }
      } else return;
    }

  }
})();