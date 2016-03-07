/**
 * Map controller
 * @namespace app
 */

(function () {
    'use strict';

    app.controller('MapController', MapController);

    MapController.$inject = ['uiGmapGoogleMapApi', 'Ndt', 'Isp', 'GeoLocation', '$log', '$scope', '$filter', 'toaster'];

    /**s
     * @namespace MapController
     * @param uiGmapGoogleMapApi
     * @param Ndt Service
     * @param GeoLocation Service
     * @param $log logging service
     * @param $scope for watching filters
     * @param $filter for filters map markers
     */
    function MapController(uiGmapGoogleMapApi, Ndt, Isp, GeoLocation, $log, $scope, $filter, toaster) {
        var vm = this;
        var logger = $log.getInstance('MapController');
        vm.getAverage = getAverage;
        vm.updateCharts = updateCharts;
        vm.loadLineGraphUpload = loadLineGraphUpload;
        vm.loadLineGraphDownload = loadLineGraphDownload;
        vm.applyFilters = applyFilters;
        vm.nullIsp = true;
        vm.ispFilterEvents = {
            onItemDeselect: function() {
                applyFilters([vm.ispFilterList, vm.priceSlider, vm.downloadSlider, vm.uploadSlider]);
            },
            onDeselectAll: function() {
               applyFilters([[], vm.priceSlider, vm.downloadSlider, vm.uploadSlider]);
            },
            onItemSelect: function(item) {
                angular.forEach(vm.ispList, function(isp) {
                    if (item.id == isp.id) {
                        vm.ispFilterList[vm.ispFilterList.indexOf(item)] = isp;
                    }
                });
                applyFilters([vm.ispFilterList, vm.priceSlider, vm.downloadSlider, vm.uploadSlider]);
            }
        };
        vm.ispFilterList = [];
        vm.ispList = [];
        vm.ispFilterTranslations = {
            buttonDefaultText: $filter('translate')('map.filter.SELECT'),
            dynamicButtonTextSuffix: $filter('translate')('map.filter.CHECKED'),
            uncheckAll: $filter('translate')('map.filter.UNCHECK_ALL')
        };
        vm.ispFilterSettings = {
            scrollableHeight: '150px',
            scrollable: true,
            showCheckAll: false,
            displayProp: 'name',
            showUncheckAll: true
        };
        vm.currentZoom = 13;
        vm.firstLaunch = true;
        vm.drawMap = drawMap;
        vm.createCharts = createCharts;
        vm.pieChartData = pieChartData;
        vm.markerComparator = markerComparator;
        vm.map = '';
        vm.defaultCoordinates = {lat:35.734398, lng:51.381359}; //Tehran {lat:43.657269, lng:-79.388395}; //Toronto //
        vm.currentCoordinates = vm.defaultCoordinates;
        vm.downloadSlider = [0, 100];
        vm.uploadSlider = [0, 100];
        vm.priceSlider = [0, 300000];
        vm.averagePrice = 0;
        vm.averageDownload = 0;
        vm.averageUpload = 0;
        vm.totalNumber = 0;
        vm.averageLatency = 0;
        vm.refreshCharts = true;
        vm.geoOptions = {
            enableHighAccuracy: false, //true slower response time, use GPS
            timeout: 5000, // Wait 5 seconds for the device to respond
            maximumAge: 1000*60*30 //  Cached position of the device is valid for 30 minutes
        };
        activate();
        var app_content_height = document.getElementById('app-content').clientHeight;
        var chart_height = document.getElementById('charts').clientHeight;
        var h = Math.min(app_content_height, chart_height-20); //20 is the extra margin of charts which is not visible
        angular.element(".angular-google-map-container").css('height', h);

        function activate() {
            Isp.list().then(function(data) {
               logger.info('List of ISPs for the multiselect dropdown retrieved.');
               vm.ispList =  data.data;
               angular.forEach(vm.ispList, function(isp){
                   vm.ispFilterList.push(isp);
               });
            });
            var storedLocation = JSON.parse(localStorage.getItem('currentPosition'));
            if (storedLocation == null)
            {
                GeoLocation.getLocation(vm.geoOptions).then(getPositionSuccess, getPositionError);
            }
            else
            {
                vm.currentCoordinates = {lat: storedLocation.latitude, lng: storedLocation.longitude};
                drawMap(vm.currentCoordinates);
            }
        }

        function applyFilters(filterValues) {
            vm.markers = $filter("ispFilter")(vm.markersOrig, filterValues, vm.nullIsp);
            var stats = vm.getAverage(vm.markers);
            vm.totalNumber = stats[0];
            vm.averageDownload = stats[1];
            vm.averageUpload = stats[2];
            vm.averagePrice = stats[3];
            vm.updateCharts();
        }

        $scope.$watchGroup(['vm.ispFilterList', 'vm.priceSlider', 'vm.downloadSlider', 'vm.uploadSlider', 'vm.nullIsp'], function(filterValues) {
            applyFilters(filterValues);
        });


        /**
         * callback function to get current geolocation
         * @param position current gelocate position
         */
        function getPositionSuccess(position) {
            logger.info("Latitude: " + position.coords.latitude +" Longitude: " + position.coords.longitude);
            vm.currentCoordinates = {lat: position.coords.latitude, lng: position.coords.longitude};
            drawMap(vm.currentCoordinates);
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

        /**
         * @name getTestResultsSuccessFn
         * @desc shows the success message
         */
        function getTestResultsSuccessFn(data, status, headers, config) {
            vm.markersOrig = data.data;
            for (var i = 0; i < data.data.length; i++) {
                var glocation = data.data[i]['location'];
                var regExp = /\(([^)]+)\)/;
                if (glocation !== null) {
                    var arrayOfStrings = regExp.exec(glocation)[1].split(" ");
                    if (arrayOfStrings !== null) {
                        vm.markersOrig[i]['latitude'] = Number(arrayOfStrings[0]);
                        vm.markersOrig[i]['longitude'] = Number(arrayOfStrings[1]);
                    }
                }
            }
            applyFilters([vm.ispFilterList, vm.priceSlider, vm.downloadSlider, vm.uploadSlider]);
            if (vm.firstLaunch) {
                vm.createCharts();
                vm.firstLaunch = false;
            } else {
                vm.updateCharts();
            }
        }

        /**
         * @name getTestResultsErrorFn
         * @desc shows the error message
         */
        function getTestResultsErrorFn(data, status, headers, config) {
             var msg= '<span>' + $filter('translate')('errors.ERROR_TEST_RESULT_LOAD') + '</span>';
             toaster.pop('warning', $filter('translate')('errors.ERROR'), msg, 5000, 'trustedHtml')
        }

        /**
         * In order to use Javascript sort function we need to define how marker objects should
         * be compared. This function takes a parameter (upload rate, download rate etc) and sort
         * the marker objects by that property
         * @param property
         * @returns {Function}
         */
        function markerComparator(property) {
            return function(a, b) {
                return a[property] - b[property];
            };
        }

        function loadLineGraphUpload() {
            if (vm.markersOrig) {
                vm.markersOrig.sort(vm.markerComparator('upload_rate'));
                var lineGraphUpload = new Array(10);
                var categories = [];
                for (var k = 0; k < 11; k++) lineGraphUpload[k] = 0;
                lineGraphUpload[0] = $filter('translate')('map.uploadHistogram.UPLOAD_RATE');
                if (vm.markers.length != 0) {
                    var upload_diff = (vm.markersOrig[vm.markersOrig.length - 1]['upload_rate'] - vm.markersOrig[0]['upload_rate']) / 10;
                    var minRange = vm.markersOrig[0]['upload_rate'];
                    var maxRange = minRange + upload_diff;
                    for (var m = 1; m < 11; m++) {
                        for (var i = 0; i < vm.markers.length; i++) {
                            if (vm.markers[i]['upload_rate'] >= minRange && vm.markers[i]['upload_rate'] <= maxRange) {
                                lineGraphUpload[m]++;
                            }
                        }
                        categories.push(maxRange.toFixed(0));
                        minRange = maxRange;
                        maxRange = minRange + upload_diff;
                    }
                }
                return [categories, lineGraphUpload];
            }
        }

        function loadLineGraphDownload() {
            if (vm.markersOrig) {
                vm.markersOrig.sort(vm.markerComparator('download_rate'));
                var lineGraphDownload = new Array(10);
                var categories = [];
                for (var k = 0; k < 11; k++) lineGraphDownload[k] = 0;
                lineGraphDownload[0] = $filter('translate')('map.downloadHistogram.DOWNLOAD_RATE');
                if (vm.markers.length != 0) {
                    var download_diff = (vm.markersOrig[vm.markersOrig.length - 1]['download_rate'] - vm.markersOrig[0]['download_rate']) / 10;
                    var minRange = vm.markersOrig[0]['download_rate'];
                    var maxRange = minRange + download_diff;
                    for (var m = 1; m < 11; m++) {
                        for (var i = 0; i < vm.markers.length; i++) {
                            if (vm.markers[i]['download_rate'] >= minRange && vm.markers[i]['download_rate'] <= maxRange) {
                                lineGraphDownload[m]++;
                            }
                        }
                        categories.push(maxRange.toFixed(0));
                        minRange = maxRange;
                        maxRange = minRange + download_diff;
                    }
                }
                return [categories, lineGraphDownload];
            }
        }

        function pieChartData() {
            var subValue = 0;
            var total = 1;
            if (vm.markers && vm.markersOrig) {
                subValue = vm.markers.length;
                total = vm.markersOrig.length;
            }
            return (subValue/total)*100;
        }

        function createCharts(){
            var uploadValues = vm.loadLineGraphUpload();
            vm.uploadHistogram = c3.generate({
                bindto: '#uploadHistogram',
                padding: {
                    top:10,
                    right: 10,
                    bottom: 0,
                    left: 40
                },
                data: {
                    columns: [
                      uploadValues[1]
                    ],
                    type: 'bar',
                    labels: false,
                    colors: {
                        upload_rate: '#ccccff'
                    }
                },
                legend: {
                    position: 'inset',
                    inset: {
                        anchor: 'top-right'
                    }
                },
                axis: {
                    x: {
                        label: {
                            position: 'outer-center',
                            text: $filter('translate')('general.MBPS')
                        },
                        type: 'category',
                        categories: uploadValues[0]
                    }
                },
                bar: {
                    width: {
                        ratio: 1 // this makes bar width 50% of length between ticks
                    }
                }
            });
            var downloadValues = vm.loadLineGraphDownload();
            vm.downloadHistogram = c3.generate({
                bindto: '#downloadHistogram',
                padding: {
                    top:10,
                    right: 10,
                    bottom: 0,
                    left: 40
                },
                data: {
                  columns: [
                    downloadValues[1]
                  ],
                  type: 'bar',
                  colors: {
                      download_rate: '#ffcccc'
                  }
                },
                legend: {
                    position: 'inset',
                    inset: {
                        anchor: 'top-right'
                    }
                },
                axis: {
                    x: {
                        type: 'category',
                        label: {
                            position: 'outer-center',
                            text: $filter('translate')('general.MBPS')
                        },
                        categories: downloadValues[0]
                    }
                },
                bar: {
                    width: {
                        ratio: 1 // this makes bar width 50% of length between ticks
                    }
                }
            });

            vm.barChart = c3.generate({
                bindto: '#barChart',
                padding: {
                    top:10,
                    right: 10,
                    bottom: 10,
                    left: 40
                },
                data: {
                    columns: [
                        [$filter('translate')('map.barChart.UNFILTERED_TESTS'), vm.markers.length],
                        [$filter('translate')('map.barChart.TOTAL'), vm.markersOrig.length]
                    ],
                    type: 'bar'
                },
                axis: {
                    x: {
                        type: 'category',
                        tick: {
                            fit: true
                        }
                    },
                    y: {
                        tick: {
                            values: [0, (vm.markersOrig.length/5).toFixed(0), ((vm.markersOrig.length/5).toFixed(0))*2, (vm.markersOrig.length/5).toFixed(0)*3, (vm.markersOrig.length/5).toFixed(0)*4, (vm.markersOrig.length/5).toFixed(0)*5],
                            count: 5
                        }
                    }
                },
                bar: {
                    width: {
                        ratio: 0.5 // this makes bar width 50% of length between ticks
                    }
                }
            });

            vm.pieChart = c3.generate({
                bindto: '#pieChart',
                padding: {
                    top:10,
                    right: 10,
                    bottom: 10,
                    left: 10
                },
                data: {
                    columns: [
                        [$filter('translate')('map.pieChart.UNFILTERED'), pieChartData()],
                        [$filter('translate')('map.pieChart.FILTERED'), 100 - pieChartData()]
                    ],
                    type : 'pie'
                },
                color: {
                  pattern: ['#1f77b4', '#aec7e8']
                }
            });
        }

        /**
         * Loads new values into each of the charts
         * This function is called whenever the filter values change
         */
        function updateCharts(){
            var uploadValues = vm.loadLineGraphUpload();
            if (vm.uploadHistogram) {
                vm.uploadHistogram.load({
                    columns: [
                        uploadValues[1]
                    ]
                });
            }
            var downloadValues = vm.loadLineGraphDownload();
            if (vm.downloadHistogram) {
                vm.downloadHistogram.load({
                    columns: [
                        downloadValues[1]
                    ]
                });
            }
            if (vm.barChart) {
                vm.barChart.load({
                    columns: [
                        [$filter('translate')('map.barChart.UNFILTERED_TESTS'), vm.markers.length],
                        [$filter('translate')('map.barChart.TOTAL'), vm.markersOrig.length]
                    ]
                });
            }
            if (vm.pieChart) {
                vm.pieChart.load({
                    columns: [
                        [$filter('translate')('map.pieChart.UNFILTERED'), pieChartData()],
                        [$filter('translate')('map.pieChart.FILTERED'), 100 - pieChartData()]
                    ]
                })
            }
            vm.refreshCharts = ! vm.refreshCharts;
        }

        function getAverage(){
            var download=0, upload=0, price=0, n=0;
            angular.forEach(vm.markers, function (marker) {
                download += marker.download_rate;
                upload += marker.upload_rate;
                price += Number(marker.price); // price is integer
                n+=1;
            });
            if (n==0) return [0,0,0,0];
            return [n, download/n, upload/n, price/n];
        }

        function reloadMap(maps) {
            var bounds = maps.getBounds();
            var xmin = bounds.getNorthEast().lat();
            var ymin = bounds.getSouthWest().lng();
            var xmax = bounds.getSouthWest().lat();
            var ymax = bounds.getNorthEast().lng();
            Ndt.getTestResultsRect(xmin, ymin, xmax, ymax).then(getTestResultsSuccessFn, getTestResultsErrorFn);
        }

        function drawMap(coordinates){
            uiGmapGoogleMapApi.then(function () {
                vm.map = {
                    options: {
                        zoomControl: true,
                        draggable: true,
                        navigationControl: false,
                        mapTypeControl: false,
                        scaleControl: false,
                        streetViewControl: false,
                        disableDoubleClickZoom: false,
                        keyboardShortcuts: false,
                        zoom: vm.currentZoom,
                        styles : [{
                            stylers: [
                                {visibility: "simplified"},
                                {saturation: -50}
                            ]
                        }]
                    },
                    center: {
                        latitude: coordinates.lat,
                        longitude: coordinates.lng
                    },
                    events: {
                        tilesloaded: function (maps, eventName, args) {
                            if (vm.firstLaunch) {
                                reloadMap(maps);
                            }
                        },
                        dragend: function (maps, eventName, args) {
                            reloadMap(maps);
                        },
                        zoom_changed: function (maps, eventName, args) {
                            reloadMap(maps);
                        }
                    }
                };
            });
        }
    }
})();
