/**
 * Report
 * @namespace ndtApp.report.services
 */
(function () {
  'use strict';

  angular
    .module('ndtApp.reports.services')
    .factory('Report', Report);

  Report.$inject = ['$http', '$translate', '$filter', 'notify', '$log'];

  /**
   * @namespace Report
   * @returns {Factory}
   */
  function Report($http, $translate, $filter, notify, $log) {
    /**
     * @name Report
     * @desc The Factory to be returned
     */
    var Report = {
       // This is personal preference, but I find it's more readable to define your service
       // as a named object and then return it, we expose this utilises by this method as a part of our service
      register: register
    };

    return Report;

    /**
    * @name register
    * @desc Try to register a new user
    * @param {data} An object with several properties listed here
    * @returns {Promise}
    * @memberOf ndtApp.report.services.Report
    */
    function register(data) {
      return $http.post('/ndt/profile/', {
          country: data.country,
          province : data.province,
          city : data.city,
          ISP: data.ISP,
          service_type: data.serviceType,
          name: 'Anonymous',  // TODO: get this name from a logged in user in future
          nominal_download_rate: data.nominal_download_rate,
          nominal_upload_rate: data.nominal_upload_rate,
          general_rating: data.rate_overall,
          customer_rating: data.rate_customerService,
          firewall: data.firewall,
          bandwidth: data.bandwidth,
          comment: data.comment,
          promotion: data.promotion,
          price: data.price,
          vpn: data.vpn
          }).then(registerSuccessFn, registerErrorFn);

      /**
      * @name registerSuccessFn
      * @desc Log the new user in
      */
      function registerSuccessFn(data, status, headers, config) {
         if (data.data.message && data.data.status) {
             var msg = '<span><strong>' + data.data.status + ': </strong>' + data.data.message + '</span>';
             notify({
                 messageTemplate: msg,
                 duration: '3000',
                 classes: "alert-success"
             });
         }
         else {
             $log.debug('registerSuccessFn: No proper data was returned from the server');
         }
      }

      /**
      * @name registerErrorFn
      * @param data is object which has data, status, headers, config, statusText
      */
      function registerErrorFn(data) {
        if (data.data.message && data.data.status){
            var msg= '<span><strong>' + data.data.status+ ': </strong>' + data.data.message+ '</span>';
            notify({
                    messageTemplate :msg,
                    duration : '0',
                    classes : "alert-danger"
                });
        } else {
            var msg = $filter('translate')('INTERNAL_ERROR')
            notify({
                message: msg,
                duration: '0',
                classes: "alert-danger"
            });
        }
      }
    }

 
  }
})();
