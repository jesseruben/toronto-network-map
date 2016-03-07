/**
 * Contact controller
 * @namespace app.contact.controllers
 */

(function () {
  'use strict';

  app.controller('ContactController', ContactController);

  ContactController.$inject = ['Contact', '$translate', '$filter', '$log', 'toaster'];

  /**
   * @namespace ContactController
   * @param Contact Service
   */
  function ContactController(Contact, $translate, $filter, $log, toaster) {
      var vm = this;
      vm.sendMessage = sendMessage;

      function sendMessage() {
          Contact.sendMessage(vm.name, vm.email, vm.subject, vm.message).then(contactSuccessFn).catch(contactErrorFn);

          function contactSuccessFn(data){
             toaster.pop('success', $filter('translate')('contact.CONTACT_US'), $filter('translate')('contact.SUCCESS'), 5000, 'trustedHtml')
          }

          function contactErrorFn(data){
             toaster.pop('warning', $filter('translate')('errors.INTERNAL_SERVER_ERROR'), $filter('translate')('errors.DATA_NOT_SUBMITTED'));
          }
      }

      vm.getError = function(error, min, max) {
        if (angular.isDefined(error)){
            if (error.required){
                return $filter('translate')('errors.ERROR_REQUIRED');
            } else if (error.email){
                return $filter('translate')('errors.ERROR_EMAIL');
            } else if (error.minlength){
                return $filter('translate')('errors.ERROR_SHORT')+ min;
            } else if (error.maxlength) {
                return $filter('translate')('errors.ERROR_LONG') + max;
            } else if (error.alphanumeric){
                return $filter('translate')('errors.ERROR_ALPHA_NUMERIC');
            }
        }
      }
  }
})();
