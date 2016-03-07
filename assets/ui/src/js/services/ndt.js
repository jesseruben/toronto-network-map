/**
 * Ndt
 * @namespace ndtApp.ndt.services
 */
(function () {
  'use strict';

  angular
    .module('app')
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
      getTestResultsCircle: getTestResultsCircle,
      getTestResultsRect: getTestResultsRect
    };

    function getTestResultsCircle(latitude, longitude, dist) {
      logger.debug('getTestResultsCircle is called to get the test results in a circle with the center = (latitude, longitude) and radius=dist');
      var url = '/stats/regionalCircle/';
      var params = {};
      params.dist = dist;
      params.latitude = latitude;
      params.longitude = longitude;
      return $http.get(url, {params: params});
    }

    function getTestResultsRect(xmin, ymin, xmax, ymax) {
      logger.debug('getResults is called to get the test results.');
      var url = '/stats/regionalRect/';
      var params = {};
      params.xmin = xmin;
      params.ymin = ymin;
      params.xmax = xmax;
      params.ymax = ymax;
      return $http.get(url, {params: params});
    }

    return ndt;
  }
})();
