/**
 * Ndt
 * @namespace ndtApp.ndt.services
 */
(function () {
  'use strict';

  angular
    .module('ndtApp.ndt.services')
    .factory('Ndt', Ndt);

  Ndt.$inject = ['$http', '$log'];

  /**
   * @namespace MapResults
   * @returns {Factory}
   */
  function Ndt($http, $log) {
    var logger = $log.getInstance('Ndt service');
    /**
     * @name MapResults
     * @desc The Factory to be returned
     */
    var ndt = {
      getResults: getResults
    };

    function getResults() {
      logger.debug('getResults is called to get the test results.');
      return $http.get('/ndt/test/');
    }

    return ndt;
  }
})();
