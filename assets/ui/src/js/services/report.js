/**
 * Report
 * @namespace report
 */
(function () {
  'use strict';

  angular
    .module('report', [])
    .factory('Report', Report);

  Report.$inject = ['$http', '$translate', '$filter', '$log'];

  /**
   * @namespace Report
   * @returns {Factory}
   */
  function Report($http, $translate, $filter, $log) {
    /**
     * @name Report
     * @desc The Factory to be returned
     */
    var Report = {
       // This is personal preference, but I find it's more readable to define your service
       // as a named object and then return it, we expose this utilises by this method as a part of our service
      submit: submit
    };

    return Report;

    /**
    * @name register
    * @desc Try to register a new user
    * @param {data} An object with several properties listed here
    * @returns {Promise}
    * @memberOf ndtApp.report.services.Report
     *
    */
    function submit(data) {
      return $http.post('/ndt/profile/', {
          service_type: data.service_type,
          name: data.name,
          nominal_download_rate: data.nominal_download_speed,
          nominal_upload_rate: data.nominal_upload_speed,
          bandwidth: data.nominal_bandwidth,
          contract: data.contract,
          city: data.city,
          province: data.province,
          rating_general: data.rate_overall,
          rating_customer_service: data.rate_customerService,
          promotion: data.promotion,
          price: data.price,
          vpn: data.vpn,
          isp: data.isp,
          isp_name: data.isp_name,
          latitude: data.latitude,
          longitude: data.longitude,
          hash: data.bindingHash
         // country: data.country
      });
    }


  }
})();
