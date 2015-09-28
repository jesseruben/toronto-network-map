/**
 * Report controller
 * With a service and interface in place, we need a controller to hook the two together
 * template is in top template folder and service is in the services folder
 * @namespace ndtApp.report.controllers
 */

(function () {
  'use strict';

  angular
    .module('ndtApp.reports.controllers')
    .controller('ReportController', ReportController);

  ReportController.$inject = ['$modalInstance', 'passedData', 'Authentication', '$translate', '$filter','Report', '$log'];

  /**
   * @namespace ModalController
   * @param passedData is the object passed by the original controller and will be available to ModalController
   * @param $modalInstance instance of the modal
   */
  function ReportController($modalInstance, passedData, Authentication, $translate, $filter, Report, $log) {
        var vm = this;
        vm.ratingMax = 5;
        vm.steps = ['one', 'two', 'three'];
        vm.step = 0;
        vm.lang = $translate.use();
        vm.rate_overall = 0;
        vm.rate_customerService = 0;
        activate();

        function activate(){
            if (Authentication.isAuthenticated()){
                vm.email = Authentication.getAuthenticatedAccount()['email'];
            }
        }
      /**
       * set rating star based on the value user is hovering over
       * @param value integer between 1-5
       * @param rating_type is the string corresponds to the name of rating, i.e. overall, customerService
       */
        vm.hoveringOver= function(value, rating_type) {
            switch (rating_type) {
                case 'overall':
                    vm.overStar_overall = value;
                    break;
                case 'customerService':
                    vm.overStart_customerService = value;
                    break;
            }
        };

        vm.isFirstStep = function () {
            return vm.step === 0;
        };

        vm.isLastStep = function () {
            return vm.step === (vm.steps.length - 1);
        };

        vm.isCurrentStep = function (step) {
            return vm.step === step;
        };

        vm.setCurrentStep = function (step) {
            vm.step = step;
        };

        vm.getCurrentStep = function () {
            return vm.steps[vm.step];
        };

        vm.getNextLabel = function () {
            return (vm.isLastStep()) ? $filter('translate')('SUBMIT') : $filter('translate')('NEXT');
        };

        vm.handlePrevious = function () {
            vm.step -= (vm.isFirstStep()) ? 0 : 1;
        };
        /*
        * Close handler is treated as success function
         */
        vm.handleNext = function () {
            if (vm.isLastStep()) {
                $modalInstance.close(vm);
            } else {
                vm.step += 1;
            }
        };

       /*
        * dismiss handler is treated as error function
        */
        vm.dismiss = function(reason) {
            $modalInstance.dismiss(reason);
        };

        vm.getError = function(error) {
          if (angular.isDefined(error)){
              if (error.required){
                  return $filter('translate')('ERROR_REQUIRED');
              } else if (error.number){
                  return $filter('translate')('ERROR_NUMBER');
              }
          } else return;
        }
  }
})();