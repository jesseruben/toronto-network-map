/**
* AccountController
* @namespace toolApp.authentication.controllers
*/
(function () {
  'use static';

  angular
    .module('ndtApp')
    .controller('AccountController', AccountController);

  AccountController.$inject = ['Authentication', '$modal', '$location', '$cookies', '$filter'];

  /**
  * @namespace AccountController
  */
  function AccountController(Authentication, $modal, $location, $cookies, $filter) {
    var vm = this;

    vm.activeProfile = false;
    vm.activeAnalytics = false;
    vm.activeUserInfo = true;
    vm.activeUpdatePassword = false;
    vm.activeDeactivation = false;

    vm.updatePassword = updatePassword;
    vm.getError = getError;
    vm.deactivationOpenModal = deactivationOpenModal;

    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated, nothing special
    * @memberOf ndtApp.authentication.controllers.AccountController
    */
    function activate() {

      // If the user is authenticated, they should not be here.

      if (!Authentication.isAuthenticated()) {
        $location.url('/login');
      }
      // Angular 1.3 syntax
      // var account = JSON.parse($cookies.authenticatedAccount);
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

    function deactivationOpenModal() {
        vm.modalInstance = $modal.open({
            templateUrl: '/static/templates/authentication/modal.html',
            controller: 'DeactivationModalController',
            controllerAs: 'vm'
        });

        /*
         When we stored the reference of our modal as modalInstance, it came with a result property
         that is actually a promise and is resolved when the modal is closed or dismissed.
        */
        vm.modalInstance.result
            .then(function (data) {
               Authentication.deactivate(data)
            },
            function (reason) {
            });
    }

    /**
    * @name getError
    * @desc Getting error for the form element
    * @memberOf ndtApp.authentication.controllers.accountController
    */
    function getError (error, min, max){
      if (angular.isDefined(error)) {
          if (error.required) {
              return $filter('translate')('ERROR_REQUIRED');
          } else if (error.pattern) {
              return $filter('translate')('ERROR_PASSWORD_REGEX');
          } else if (error.minlength){
              return $filter('translate')('ERROR_SHORT')+ min;
          } else if (error.maxlength) {
              return $filter('translate')('ERROR_LONG')+ max;
          } else if (error.pwmatch){
              return $filter('translate')('ERROR_PASSWORD_MATCH');
          }
      }
    }

  }
})();