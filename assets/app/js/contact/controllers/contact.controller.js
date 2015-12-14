/**
 * Contact controller
 * With a service and interface in place, we need a controller to hook the two together
 * template is in top template folder and service is in the services folder
 * @namespace ndtApp.contact.controllers
 */

(function () {
  'use strict';

  angular
    .module('ndtApp.contact.controllers')
    .controller('ContactController', ContactController);

  ContactController.$inject = ['Contact', '$translate', '$filter', '$log'];

  /**
   * @namespace ContactController
   * @param Contact Service
   */
  function ContactController(Contact, $translate, $filter, $log) {
      var vm = this;
      vm.sendMessage = sendMessage;

      function sendMessage() {
          Contact.sendMessage(vm.email, vm.subject, vm.message);
      }

      vm.getError = function(error, min, max) {
        if (angular.isDefined(error)){
            if (error.required){
                return $filter('translate')('ERROR_REQUIRED');
            } else if (error.number){
                return $filter('translate')('ERROR_NUMBER');
            } else if (error.email){
                return $filter('translate')('ERROR_EMAIL');
            } else if (error.minlength){
                return $filter('translate')('ERROR_SHORT')+ min;
            } else if (error.maxlength) {
                return $filter('translate')('ERROR_LONG') + max;
            }
        }
      }
  }
})();