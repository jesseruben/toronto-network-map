/**
* LoginController
* @namespace ndtApp.authentication.controllers
*/
(function () {
  'use static';

  angular
    .module('ndtApp.authentication.controllers')
    .controller('LoginController', LoginController);

  LoginController.$inject = ['Authentication', '$filter', '$log'];

  /**
  * @namespace LoginController
  */
  function LoginController(Authentication, $filter, $log) {
    var vm = this;
    vm.login = login;
    vm.getError = getError;
    vm.logout = logout;
    vm.model = {
    name: "controllerAs vm test"
    };

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated, nothing special
    * @memberOf ndtApp.authentication.controllers.LoginController
    */
    function activate() {
      // If the user is authenticated, they should not be here.
      if (Authentication.isAuthenticated()) {
        //  $location.url('/');
      }
    }

    /**
    * @name login
    * @desc Log the user in with authentication service
    * @memberOf ndtApp.authentication.controllers.LoginController
    */
    function login() {
      Authentication.login(vm.email, vm.password);
    }

    /**
    * @name logout
    * @desc Log the user out with authentication service
    * @memberOf ndtApp.authentication.controllers.LoginController
    */
    function logout() {
      Authentication.logout();
    }

    /**
    * @name getError
    * @desc Getting error for the form element
    * @memberOf ndtApp.authentication.controllers.LoginController
    */
    function getError (error){
      if (angular.isDefined(error)){
          if (error.required){
              return $filter('translate')('ERROR_REQUIRED');
          } else if (error.email){
              return $filter('translate')('ERROR_EMAIL');
          }
      }
    }

  }
})();