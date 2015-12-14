/**
 * Tools
 * @namespace ndtApp.ndt.filters
 */
(function () {
    'use strict';

    angular
        .module('ndtApp.ndt.filters')
        .filter('ispFilter',function(){
            return function(markerList, filterValues) {
                var out = [];
                var parsed;
                var dropDownIspNames = filterValues[0];
                var priceRange = filterValues[1];
                var downloadRange = filterValues[2];
                var uploadRange = filterValues[3];

                angular.forEach(markerList, function(marker) {
                    if (dropDownIspNames.length == 0){
                        // None of the dropdown list was selected = no filter
                         if (filterRange(marker,downloadRange,uploadRange,priceRange)) {
                             out.push(marker)
                         }
                    } else {
                        angular.forEach(dropDownIspNames, function(dropDownItem){
                            // dropDownIspName is passed as an array in pure string format, we can use eval function which
                            // is not safe, the other solution is using JSON.parse, otherwise we couldn't
                            // read obj.name
                            parsed= JSON.parse(dropDownItem);
                            if (marker.isp_name === parsed.name) {
                                if (filterRange(marker, downloadRange, uploadRange, priceRange)){
                                    out.push(marker)
                                }
                            }
                        })
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
                        &&
                        uploadRange[0] <= marker.upload_rate && marker.upload_rate <= uploadRange[1]
                        &&
                        priceRange[0] <= marker.price && marker.price <= priceRange[1])
                }

            }
        })
})();
