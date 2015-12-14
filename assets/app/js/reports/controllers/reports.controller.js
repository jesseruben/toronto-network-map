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

  ReportController.$inject = ['Authentication', '$translate', '$filter','Report', '$log'];

  /**
   * @namespace ModalController
   * @param passedData is the object passed by the original controller and will be available to ModalController
   */
  function ReportController(Authentication, $translate, $filter, Report, $log) {
        var vm = this;
        vm.ratingMax = 5;
        vm.lang = $translate.use();
        vm.rate_overall = 0;
        vm.rate_customerService = 0;
        vm.getError = getError;
        vm.hoveringOver = hoveringOver;
        vm.sendReport = sendReport;

        activate();

        function activate(){
            if (Authentication.isAuthenticated()){
                vm.email = Authentication.getAuthenticatedAccount()['email'];
            }
        }

       /**
        * Sends users feedback as a report to the remote server
        */
        function sendReport(){
            var data = {
                ISP: vm.ISP,
                service_type: vm.service_type,
                nominal_download_speed: vm.nominal_download_rate,
                nominal_upload_speed: vm.nominal_upload_rate,
                rate_overall: vm.rate_overall,
                rate_customerService: vm.rate_customerService,
                promotion: vm.promotion,
                vpn: vm.vpn,
                price: vm.price
            };
            Report.submit(data)
        }

      /**
       * set rating star based on the value user is hovering over
       * @param value integer between 1-5
       * @param rating_type is the string corresponds to the name of rating, i.e. overall, customerService
       */
        function hoveringOver(value, rating_type) {
            switch (rating_type) {
                case 'overall':
                    vm.overStar_overall = value;
                    break;
                case 'customerService':
                    vm.overStart_customerService = value;
                    break;
            }
        }

        function getError(error) {
          if (angular.isDefined(error)) {
              if (error.required) {
                  return $filter('translate')('ERROR_REQUIRED');
              } else if (error.number) {
                  return $filter('translate')('ERROR_NUMBER');
              }
          }
        }
  }
})();