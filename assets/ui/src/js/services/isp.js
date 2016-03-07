/**
 * Ndt
 * @namespace app.services.Isp
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('Isp', Isp);

    Isp.$inject = ['$http', '$log'];

    /**
     * @namespace MapResults
     * @returns {Factory}
     */
    function Isp($http, $log) {
        var logger = $log.getInstance('ISP service');
        /**
         * @name MapResults
         * @desc The Factory to be returned
         */
        var isp = {
            list: list,
            get: get
        };

        function list() {
            logger.debug('list is called to get isp list');
            return $http.get('/isp/providers/');
        }

        function get(id) {
            logger.debug('get is called to get isp number: '+ id);
            return $http.get('/isp/providers/' + id + '/');
        }

        return isp;
    }
})();
