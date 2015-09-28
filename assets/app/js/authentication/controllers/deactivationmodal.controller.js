/**
 * DeactivationModal controller
 * With a service and interface in place, we need a controller to hook the two together
 * template is in top template folder and service is in the services folder
 * @namespace ndtApp.authentication.controllers
 */

(function () {
  'use strict';

  angular
    .module('ndtApp.authentication.controllers')
    .controller('DeactivationModalController', DeactivationModalController);

  DeactivationModalController.$inject = ['$modalInstance'];

  /**
   * @namespace DeactivationModalController
   * @param $modalInstance instance of the modal
   */
  function DeactivationModalController($modalInstance) {
        var vm = this;
        vm.submit = submit;
        vm.dismiss = dismiss;

       /*
        * submit handler
        */
        function submit() {
            $modalInstance.close(vm.password);
        }

       /*
        * dismiss handler is treated as error function
        */
        function dismiss(reason) {
            $modalInstance.dismiss(reason);
        };
  }
})();