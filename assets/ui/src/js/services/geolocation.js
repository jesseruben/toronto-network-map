/**
 * Ndt
 * @namespace ndtApp.ndt.services
 */
(function () {
    'use strict';

    angular
        .module('GeoLocation', [])
        .constant('geolocation_msgs', {
            'errors.location.unsupportedBrowser':'Browser does not support location services',
            'errors.location.permissionDenied':'Access to the location was rejected',
            'errors.location.positionUnavailable':'Unable to determine your location',
            'errors.location.timeout':'Service timeout has been reached'})
        .factory('GeoLocation', GeoLocation);

    GeoLocation.$inject = ['$q', '$window', 'geolocation_msgs', '$log'];

    /**
     * @namespace MapResults
     * @returns {Factory}
     */
    function GeoLocation($q, $window, geolocation_msgs, $log) {
        var that = this;
        var logger = $log.getInstance('GeoLocation Service');

        /**
         * @name MapResults
         * @desc The Factory to be returned
         */
        var  GeoLocation = {
            getLocation: getLocation
        };
        return GeoLocation;

        function getLocation(options) {
            var deferred = $q.defer();
            logger.info("getLocaton function is called");
            if ($window.navigator && $window.navigator.geolocation) {
                logger.info('Browser supports geolocation');
                $window.navigator.geolocation.getCurrentPosition(getPositionSuccess, getPositionError, options);
            } else {
                logger.error('Browser does not support geolocation');
                deferred.reject(geolocation_msgs['errors.location.unsupportedBrowser']);
            }

            /**
             * @desc add the position to service returned promise
             * @param position the coordinates come from browser geolocation
             */
            function getPositionSuccess(position){
                deferred.resolve(position)
            }

            /**
             *
             * @param error retuned by browser geolocation
             */
            function getPositionError(error) {
                switch (error.code) {
                    case 1:
                        // the following is commented for future reference in case you want to broadcast an event
                        // or trigger any apply, difgest functions
                        /* $rootScope.$broadcast('error',geolocation_msgs['errors.location.permissionDenied']);
                         $rootScope.$apply(function() {
                         deferred.reject(geolocation_msgs['errors.location.permissionDenied']);
                         }); */
                        deferred.reject(geolocation_msgs['errors.location.permissionDenied']);
                        break;
                    case 2:
                        deferred.reject(geolocation_msgs['errors.location.positionUnavailable']);
                        break;
                    case 3:
                        deferred.reject(geolocation_msgs['errors.location.timeout']);
                        break;
                } //end switch
            } //end get error

            return deferred.promise;
        } //end getLocattion main function
    }
})();
