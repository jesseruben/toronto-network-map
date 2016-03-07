/**
 * Faq controller
 * @namespace app.faq.controllers
 */

(function () {
  'use strict';

  app.controller('FaqController', FaqController);

  FaqController.$inject = ['Faq', '$filter', 'toaster'];

  /**
   * @namespace FaqController
   * @param Faq Service
   */
  function FaqController(Faq, $filter, toaster) {
      var vm = this;
      vm.faqs = [];
      vm.getFaqs = getFaqs;
      activate();

      function activate() {
          vm.getFaqs();
      }

      function getFaqs() {
          Faq.getFaqs().then(getFaqsSuccessFn).catch(getFaqsErrorFn);

          function getFaqsSuccessFn(data){
             vm.faqs = data.data;
          }

          function getFaqsErrorFn(data){
             toaster.pop('warning', $filter('translate')('faq.FAQ'), $filter('translate')('faq.ISSUE_GETTING_FAQ'), 5000, 'trustedHtml')
          }
      }
  }
})();