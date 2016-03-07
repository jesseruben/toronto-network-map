/**
 * ISP
 * @namespace ndtApp.ndt.filters
 */
(function () {
    'use strict';

    angular
        .module('app')
        .filter('ispFilter',function(){
            /**
             * @description for every marker, if values are in downloadRange, uploadRange and priceRange
             * nonIspF is set to True, then if at least for one of the ispNames the marker.isp_name matches
             * the value ispF will be set to True. Marker is only pushed to out if both nonIspF and ispF are
             * true.
             * @param markerList
             * @param filterValues
             * @returns {Array}
             */
            return function(markerList, filterValues, nullIsp) {
                var out = [];
                var dropDownIspNames = filterValues[0];
                var priceRange = filterValues[1];
                var downloadRange = filterValues[2];
                var uploadRange = filterValues[3];
                var nonIspF = false;
                var ispF  = false;
                angular.forEach(markerList, function(marker) {
                    nonIspF = false;
                    ispF  = false;
                    if (filterRange(marker, downloadRange, uploadRange, priceRange)) {
                        nonIspF = true;
                    }
                    if ((!marker.isp && nullIsp==true)){
                      ispF = true;
                    } else if (dropDownIspNames.length > 0){
                        angular.forEach(dropDownIspNames, function (dropDownItem) {
                            //console.log(marker.isp==null && nullIsp==true);
                            if (marker.isp == dropDownItem.id) {
                               ispF = true;
                            }
                        });
                    }
                    if (nonIspF && ispF) {
                        out.push(marker);
                    }
                });

                return out;

                /**
                 * @description local function check ranges filter on map page
                 * @param marker
                 * @param downloadRange
                 * @param uploadRange
                 * @param priceRange
                 * @returns {boolean}
                 */
                function filterRange(marker, downloadRange, uploadRange, priceRange) {
                  return (downloadRange[0] <= marker.download_rate && marker.download_rate <= downloadRange[1]
                  && uploadRange[0] <= marker.upload_rate && marker.upload_rate <= uploadRange[1]
                  && priceRange[0] <= marker.price && marker.price <= priceRange[1]);
                }

            }
        })
})();
