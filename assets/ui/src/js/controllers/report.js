/**
 * Report controller
 * With a service and interface in place, we need a controller to hook the two together
 * template is in top template folder and service is in the services folder
 * @namespace ndtApp.report.controllers
 */

(function () {
  'use strict';

  app.controller('ReportController', ReportController);

  ReportController.$inject = ['$translate', '$filter','Report', '$log', 'Isp', 'toaster'];

  /**
   * @namespace app.ReportController
   * @param passedData is the object passed by the original controller and will be available to ModalController
   */
  function ReportController($translate, $filter, Report, $log, Isp, toaster) {
    var vm = this;
    var logger = $log.getInstance('ReportController');
    vm.ratingMax = 5;
    vm.lang = $translate.use();
    vm.rate_overall = 0;
    vm.rate_customerService = 0;
    vm.getError = getError;
    vm.hoveringOver = hoveringOver;
    vm.sendReport = sendReport;
    vm.submitted = false;
    vm.service_type = 'HOME';
    vm.isp = {originalObject:'Undefined'}; //originalObject is set by autocomplete plugin if it fails to find users' search

    activate();

    function activate(){
      getIsps().then(function() {
        logger.info('Getting list of isps for autocomplete')
      });
      vm.nominal_download_metric = 'mb';
      vm.nominal_upload_metric = 'mb';
      vm.nominal_bandwidth_metric = 'gb';

    }


    /**
     * @description: call Isp service to get list of isps and assign it to vm.isps on success
     * @returns {* list of isps}
     */
    function getIsps(){
      return Isp.list().then(listSuccessFn).catch(listErrorFn);

      function listSuccessFn(data){
        vm.isps = data.data;
        return vm.isps;
      }

      function listErrorFn(){
        logger.warn('Could not get list of isps from the service');
      }
    }

    /**
     * Sends users feedback as a report to the remote server
     */
    function sendReport(){
      var isp, isp_name, position, latitdue, longitude;
      try{
        // Autocomplete extension set the value of vm.isp, if user correctly select an ISP we have vm.isp.description
        // If the user write his own ISP we have it in vm.isp.originalObject
        // if the user fails to input any isp, the above 'Undefined' Value will be set for the isp_name
        isp = vm.isp.description.id;
        isp_name = vm.isp.description.name;
      } catch (err){
        isp_name = vm.isp.originalObject;
        isp = null;
      }

      try{
        // getting postion from localStorage set by speedtest
        position = JSON.parse(localStorage.currentPosition);
        latitdue= position['latitude'];
        longitude = position['longitude'];
      } catch (err){
        latitdue = null;
        longitude = null;
      }

      var bindingHash = localStorage.bindingHash;
      var upload_converted = vm.nominal_upload_rate;
      var download_converted = vm.nominal_download_rate;
      var bandwidth_converted = vm.nominal_bandwidth;


      if (vm.nominal_download_metric == 'kb') {
        download_converted = vm.nominal_download_rate * 0.001;
      }
      if (vm.nominal_upload_metric == 'kb') {
        upload_converted = vm.nominal_upload_rate * 0.001;
      }
      if (vm.nominal_bandwidth_metric == 'gb') {
        bandwidth_converted = vm.nominal_bandwidth * 1000;
      }

      var data = {
        isp: isp,
        isp_name: isp_name,
        name:'Anonymous',// TODO: Read profile names for authenticated users
        service_type: vm.service_type,
        nominal_download_speed: download_converted,
        nominal_upload_speed: upload_converted,
        nominal_bandwidth: bandwidth_converted,
        rate_overall: vm.rate_overall,
        rate_customerService: vm.rate_customerService,
        promotion: vm.promotion,
        vpn: vm.vpn,
        contract: vm.contract,
        price: vm.price,
        city: vm.city,
        province: vm.province,
        latitude: latitdue,
        longitude: longitude,
        bindingHash: bindingHash
        //country: vm.country,
      };
      Report.submit(data).then(reportSuccessFn).catch(reportErrorFn);

      function reportSuccessFn(data){
        vm.submitted = true;
      }

      function reportErrorFn(){
        toaster.pop('warning', $filter('translate')('errors.INTERNAL_SERVER_ERROR'), $filter('translate')('errors.DATA_NOT_SUBMITTED'));
      }

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
          return $filter('translate')('errors.ERROR_REQUIRED');
        } else if (error.number) {
          return $filter('translate')('errors.ERROR_NUMBER');
        }
      }
    }
  }
})();
