/**
 * Map controller
 * @namespace ndtApp.map.controllers
 */

(function () {
    'use strict';

    angular
        .module('ndtApp.ndt.controllers')
        .controller('MapController', MapController);

    MapController.$inject = ['uiGmapGoogleMapApi', 'Ndt', 'GeoLocation', '$log', '$scope', '$filter', '$window'];

    /**s
     * @namespace MapController
     * @param uiGmapGoogleMapApi
     * @param Ndt Service
     * @param GeoLocation Service
     * @param $log logging service
     * @param $scope for watching filters
     * @param $filter for filters map markers
     */
    function MapController(uiGmapGoogleMapApi, Ndt, GeoLocation, $log, $scope, $filter, $window) {
        var vm = this;
        var logger = $log.getInstance('MapController');

        vm.drawMap = drawMap;
        vm.getAverage = getAverage;
        vm.map = '';
        vm.defaultCoordinates = {lat:43.6622676, lang:-79.406861}; //Toronto
        vm.priceSlider = [0, 100];
        vm.downloadSlider = [0, 50];
        vm.uploadSlider = [0, 20];
        vm.averagePrice = 0;
        vm.averageDownload = 0;
        vm.averageUpload = 0;
        vm.totalNumber = 0;
        vm.averageLatency = 0;
        vm.MapOptions = {
            zoomControl: true,
            zoom: 2,
            draggable: true,
            navigationControl: false,
            mapTypeControl: false,
            scaleControl: false,
            streetViewControl: false,
            disableDoubleClickZoom: false,
            keyboardShortcuts: false,
            styles : [{
                stylers: [
                    {visibility: "simplified"},
                    {saturation: -40}
                ]
            }]
        };
        vm.geoOptions = {
            enableHighAccuracy: false, //true slower response time, use GPS
            timeout: 5000, // Wait 5 seconds for the device to respond
            maximumAge: 1000*60*30 //  Cached position of the device is valid for 30 minutes
        };

        // list of all isps on the template
        // @todo should populate this with http
        vm.ispFilterOptions = {
            isps: [
                {name : 'Rogers'},
                {name : 'Bell'},
                {name : 'Techsavy'},
                {name : 'Acanac'}
            ]
        };

        //Mapped to dropdown menu on the template
        vm.selectedIsps = [];

        activate();
        var h= $window.innerHeight;
        angular.element(".angular-google-map-container").css('height', h-85);
        function activate() {
            GeoLocation.getLocation(vm.geoOptions).then(getPositionSuccess, getPositionError);
            Ndt.getResults().then(getResultsSuccessFn, getResultsErrorFn);
        }


        // We can't put filter on template because of digest error so we have to watch the dropdown and apply filter
        // the ispList is the list selected in dropdown menu which is mapped by selectedIsps, it is actually should be
        // written as function(newValue, oldValue)
        $scope.$watchGroup(['vm.selectedIsps', 'vm.priceSlider', 'vm.downloadSlider', 'vm.uploadSlider'], function(filterValues){
            vm.markers = $filter("ispFilter")(vm.markersOrig, filterValues);
            var stats = vm.getAverage(vm.markers);
            vm.totalNumber = stats[0];
            vm.averageDownload = stats[1];
            vm.averageUpload = stats[2];
            vm.averagePrice = stats[3];
            if (!vm.markers){
                return;
            }
        });


        /**
         * callback function to get current geolocation
         * @param position current gelocate position
         */
        function getPositionSuccess(position) {
            logger.info("Latitude: " + position.coords.latitude +" Longitude: " + position.coords.longitude);
            //drawMap({lat:position.coords.latitude, lang:position.coords.longitude});
            drawMap(vm.defaultCoordinates);
        }

        /**
         * callback function to get current geolocation error
         * @param error assed by geolocation service
         * @todo set ip geolocation here
         */
        function getPositionError(error){
            // draw a map with a predefined center
            logger.error(error);
            drawMap(vm.defaultCoordinates);
        }

        /*setTimeout(function () {
             if(!latLng){
                window.console.log("No confirmation from user, using fallback");
                getPositionError("no reaction from the user")
             }else{
                window.console.log("Location was set");
             }
         }, geoOptions.timeout + 1000); // Wait extra second
         */

        /**
         * @name getResultsSuccessFn
         * @desc shows the success message
         */
        function getResultsSuccessFn(data, status, headers, config) {
            vm.markers = data.data;
            var stats = vm.getAverage(vm.markers);
            vm.totalNumber = stats[0];
            vm.averageDownload = stats[1];
            vm.averageUpload = stats[2];
            vm.averagePrice = stats[3];
            vm.markersOrig = data.data;
        }

        function getAverage(markers){
            var download=0, upload=0, price=0, n=0;
            angular.forEach(vm.markers, function (marker) {
                download += marker.download_rate;
                upload += marker.upload_rate;
                price += parseFloat(marker.price); // price is integer
                n+=1;
            });
            if (n==0) return [0,0,0,0]
            return [n, download/n, upload/n, price/n];
        }

        /**
         * @name getResultsErrorFn
         * @desc shows the error message
         */
        function getResultsErrorFn(data, status, headers, config) {
            //pass
        }

        function drawMap(coordinates){
            uiGmapGoogleMapApi.then(function (maps) {
                vm.map = {
                    center: {
                        latitude: coordinates.lat,
                        longitude: coordinates.lang
                    },
                    zoom: 13,
                    pan: 1,
                    options: vm.MapOptions,
                    control: {},
                    events: {
                        tilesloaded: function (maps, eventName, args) {},
                        dragend: function (maps, eventName, args) {},
                        zoom_changed: function (maps, eventName, args) {}
                    }
                };
            });
        }

    }
})();
