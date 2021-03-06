'use strict';

/**
 * @ngdoc function
 * @name SpeedtestController
 * @description
 * # SpeedtestController
 * Controller of the speedtest
 */


app.controller('SpeedtestController', SpeedtestController);

SpeedtestController.$inject = ['$scope', 'Speedtest', '$filter', 'GeoLocation', '$log'];


function SpeedtestController($scope, Speedtest, $filter, GeoLocation, $log) {
  var vm = this;
  var logger = $log.getInstance('SpeedtestController');
  var blank = '<i class="fa fa-minus"></i>'; // default blank icon
  vm.serverList = [];
  vm.activeHelp = 1;
  vm.testButtonLabel = $filter('translate')('home.test.TEST_SPEED_BUTTON');
  /* Controller variables*/
  vm.iterator = 0; //keeps track of server array to test
  vm.showAverage = false; //If ture the average row will be shown on the view
  vm.status = '';
  vm.port = '3001';
  vm.path = '/ndt_protocol';
  vm.meter = undefined;
  vm.arc = undefined;
  vm.state = undefined;
  vm.body_element = '#svg'; // html ID of the place to put D3 gage
  vm.time_switched = undefined;
  vm.testInProgress = false;
  vm.downloadRates = [];
  vm.uploadRates = [];
  vm.latencyRates = [];
  vm.bindingHash = '';
  vm.refreshSpline = true;
  vm.NDT_STATUS_LABELS = {
    'preparing_s2c': $filter('translate')('home.test.PREPARING_DOWNLOAD'),
    'preparing_c2s': $filter('translate')('home.test.PREPARING_UPLOAD'),
    'running_s2c': $filter('translate')('home.test.MEASURING_DOWNLOAD'),
    'running_c2s': $filter('translate')('home.test.MEASURING_UPLOAD'),
    'finished_s2c': $filter('translate')('home.test.FINISHED_DOWNLOAD'),
    'finished_c2s': $filter('translate')('home.test.FINISHED_UPLOAD'),
    'preparing_meta': $filter('translate')('home.test.PREPARING_METADATA'),
    'running_meta': $filter('translate')('home.test.SENDING_METADATA'),
    'finished_meta': $filter('translate')('home.test.FINISHED_METADATA'),
    'finished_all': $filter('translate')('home.test.RUN_AGAIN')
  };
  vm.graphIterations = 0;
  vm.instantUploadSpeed = [];
  vm.instantDownloadSpeed = [];
  vm.downloadAverage = getAverage(vm.downloadRates);
  vm.uploadAverage = getAverage(vm.uploadRates);
  vm.latencyAverage = getAverage(vm.latencyRates);
  vm.averageRegionalUploadSpeed = [];
  vm.averageRegionalDownloadSpeed = [];
  vm.filterDistance = 1000000;
  vm.currentLatitude = '';
  vm.currentLongitude = '';
  vm.geoOptions = {
    enableHighAccuracy: false, //true slower response time, use GPS
    timeout: 5000, // Wait 5 seconds for the device to respond
    maximumAge: 1000*60*30 //  Cached position of the device is valid for 30 minutes
  };
  /* End of Variables */

  /* Functions declaration */
  vm.meter_movement = meter_movement;
  vm.update_display = update_display;
  vm.startTest = startTest;
  vm.d3Create = d3Create;
  vm.open = open;
  vm.reset_meter = reset_meter;
  vm.callbacks = {
    'onstart': onstart,
    'onstatechange': onstatechange,
    'onprogress': onprogress,
    'onfinish': onfinish,
    'onerror': onerror
  };
  vm.getRecordedTests = getRecordedTests;
  vm.getServers = getServers;
  vm.recordedTests = 0;
  activate();


  function activate(){
    getServers();
    d3Create();
    getRecordedTests();
  }

  function getServers() {
    Speedtest.getServers().then(getServersSuccess, getServersError);

    function getServersSuccess(data, status, headers, config){
      vm.serverList = data.data;
    }

    function getServersError(data, status, headers, config){
      // TODO: log the error
      // pass
    }
  }

  function getRecordedTests() {
    Speedtest.getRecordedTests().then(getRecordedTestsSuccess, getRecordedTestsError);

    function getRecordedTestsSuccess(data, status, headers, config){
      vm.recordedTests = data.data;
    }

    function getRecordedTestsError(data, status, headers, config){
      // TODO: log the error
      // pass
    }
  }

  /**
   *  Starts the NDT service
   */
  function startTest () {
    vm.bindingHash = '';
    vm.iterator = 0;
    for (var i=0; i < vm.serverList.length; i++)
    {
      vm.serverList[i].downloadSpeed = blank;
      vm.serverList[i].uploadSpeed = blank;
      vm.serverList[i].latency = blank;
    }
    vm.downloadAverage = getAverage(vm.downloadRates);
    vm.uploadAverage = getAverage(vm.uploadRates);
    vm.latencyAverage = getAverage(vm.latencyRates);
    vm.showAverage = false;
    vm.testInProgress = true;
    vm.testButtonLabel = $filter('translate')('home.test.TEST_IN_PROGRESS');
    logger.info("startTest function: testing number: %s", vm.iterator+1);

    //------------------ Reading the Location ------------------------------
    var storedLocation = JSON.parse(localStorage.getItem('currentPosition'));
    if (storedLocation == null)
    {
      GeoLocation.getLocation(vm.geoOptions).then(getPositionSuccess).catch(getPositionError);
    }
    else
    {
      vm.currentLatitude = storedLocation.latitude;
      vm.currentLongitude = storedLocation.longitude;
    }

    /**
     * @description: set the position to vm variables and localStorage
     * @param position from browser
     */
    function getPositionSuccess(position){
      vm.currentLatitude = position.coords.latitude;
      vm.currentLongitude = position.coords.longitude;
      var position = {latitude:position.coords.latitude, longitude:position.coords.longitude};
      localStorage.setItem('currentPosition', JSON.stringify(position));
    }

    function getPositionError(){
      // pass
    }
     //------------------ End of Reading the Location ------------------------------

    Speedtest.startTest(vm.serverList[vm.iterator].url, vm.port, vm.path, vm.callbacks, 1000);

  }

  /**
   *  Calculates the average of an array
   * @param rates arrays od download and upload rates
   * @returns {blank font awesome icon, average of the array with one decimal point}
   */
  function getAverage(rates){
    if (rates.length === 0) {
      return  '<i class="fa fa-minus"></i>';
    }
    var sum = 0;
    for (var i = 0;  i < rates.length; i++){
      sum += parseFloat(rates[i]);
    }
    var average = sum / rates.length;
    return average.toFixed(1);
  }

  /**
   *  Creates a d3 gage on the view, it has access to vm.body_element which define the html id of gage
   */
  function d3Create(){
    var width = 240;
    var height = 240;
    var twoPi = 2 * Math.PI;
    var innerRad = (width * 0.35);
    var outerRad = (width * 0.45);

    var svg = d3.select('#svg').append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var gradient = svg
      .append("radialGradient")
      .attr("id", "gradient")
      .attr("gradientUnits", "userSpaceOnUse");

    gradient
      .append("stop")
      .attr("offset", "0%")
      .attr("stop-color", "white");
    gradient
      .append("stop")
      .attr("offset", "10%")
      .attr("stop-color", "#00A99D");

    var defs = svg.append("defs");

    var filter = defs.append("filter")
      .attr("id", "dropshadow");

    filter.append("feGaussianBlur")
      .attr("in", "SourceAlpha")
      .attr("stdDeviation", 4)
      .attr("result", "blur");

    filter.append("feOffset")
      .attr("in", "blur")
      .attr("dx", 2)
      .attr("dy", 2)
      .attr("result", "offsetBlur");

    var feMerge = filter.append("feMerge");

    feMerge.append("feMergeNode")
      .attr("in", "offsetBlur");
    feMerge.append("feMergeNode")
      .attr("in", "SourceGraphic");

    vm.arc = d3.svg.arc()
      .startAngle(0)
      .endAngle(0)
      .innerRadius(innerRad)
      .outerRadius(outerRad);
    vm.meter = svg.append("g")
      .attr("id", "progress-meter")
      .attr("fill", "url(#gradient)");
    vm.meter.append("path")
      .attr("class", "background")
      .attr("d", vm.arc.endAngle(twoPi));
    vm.meter.append("path").attr("class", "foreground");
    vm.meter.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "0em")
      .attr("class", "information")
      .text("Initializing");

    vm.meter.append("circle")
       .attr("cx", function (d) { return 0; })
       .attr("cy", function (d) { return 0; })
       .attr("r", function (d) { return 82; })
       .attr("filter", "url(#dropshadow)")
       .style("fill", "00a99d");

    vm.reset_meter();
    vm.update_display($filter('translate')('home.test.READY_TO_TEST'), '');

    d3.selectAll("#progress-meter text").classed("ready", true);
    d3.selectAll("#progress-meter .foreground").classed("complete", true);
    d3.selectAll("#progress-meter").classed("progress-error", false);
  }


  /**
   * Reset the d3 meter and remove all status texts
   */
  function reset_meter() {
    d3.selectAll('#progress-meter text').remove();

    vm.meter.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "0em")
      .attr("font-size","14px")
      .attr("font-family", "terafik, 'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif")
      .attr("class", "status");
    vm.meter.append("text")
      .attr("text-anchor", "middle")
      .attr("dy", "1.2em")
      .attr("class", "information");

    d3.selectAll('.result_value, .result_label').remove();
    d3.select('#progress-meter').classed('progress-complete', false);
    d3.selectAll("#progress-meter text").classed("ready", true);
  }


  /**
   *
   * @param status is the current state of ndt test
   * @param information is any extra information for display purposes
   */
  function update_display (status, information) {
    update_svg_display(status);

    if (information == undefined){
      information = '';
    }

    if(!$scope.$$phase) {
      $scope.$apply(function () {
        vm.status = status + ' ' + information;
      });
    } else {
      vm.status = status + ' ' + information;
    }
  }


  function update_svg_display(status) {
    if (status == $filter('translate')('home.test.CONNECTING_TO'))
    {
      status = status + ' ' + vm.serverList[vm.iterator].name;
    }

    if (status == 'Latency')
    {
      status = $filter('translate')('home.test.DONE');
    }
    d3.select('text.status').text(status);
  }


  /**
   * Simulates the download and upload movement on the gage
   * @returns {boolean}
   */
  function meter_movement () {
    var end_angle,
      start_angle,
      progress_percentage;
    var origin = 0;
    var progress = 0;
    var twoPi = 2 * Math.PI;
    var time_in_progress = new Date().getTime() - vm.time_switched;

    if (vm.state === "running_s2c" || vm.state === "running_c2s") {
      progress_percentage = (time_in_progress < 10000) ?
        (time_in_progress / 10000) : 1;
      progress = twoPi * progress_percentage;
      if (vm.state === "running_c2s") {
        progress = twoPi + -1 * progress;
        end_angle = vm.arc.endAngle(twoPi);
        start_angle = vm.arc.startAngle(progress);
      } else {
        end_angle = vm.arc.endAngle(progress);
        start_angle = vm.arc.startAngle(origin);
      }
    } else if (vm.state === "finished_all") {
      end_angle = vm.arc.endAngle(twoPi);
      start_angle = vm.arc.startAngle(origin);
    } else {
      end_angle = vm.arc.endAngle(origin);
      start_angle = vm.arc.startAngle(origin);
    }
    d3.select('.foreground').attr("d", end_angle);
    d3.select('.foreground').attr("d", start_angle);

    return vm.state === 'finished_all';
  }

  /****    All callback functions go below this line        ****/


  /**
   * Callback function: Starts the movement of the server and update the status
   * @param server the actual server returns from the service
   */
  function onstart(server) {
    var _this = vm;
    var meter_movement = function () {
      _this.meter_movement();
    };
    d3.timer(meter_movement);
    vm.update_display($filter('translate')('home.test.CONNECTING_TO'), vm.serverList[vm.iterator].url);
  }


  /**
   * Callback function: Updates the status bar wit a received message from NDT service
   * @param returned_message comes from the service. A list of them is on top of this file in vm.NDT_STATUS_LABELS
   */
  function onstatechange(returned_message) {
    vm.state = returned_message;
    vm.time_switched = new Date().getTime();
    vm.update_display(vm.NDT_STATUS_LABELS[returned_message])
  }


  /**
   * Callback function: Updates the status bar with the progress of download and upload
   * @param returned_message contains two string showing if the service is uploading or downloading
   * @param passedResults are the download and upload rates in Kilo Bytes
   */
  function onprogress(returned_message, passedResults) {
    var throughputRate;
    var progress_label = vm.NDT_STATUS_LABELS[vm.state];

    if (returned_message === 'interval_s2c' && vm.state === 'running_s2c') {
      vm.serverList[vm.iterator].downloadSpeed = '<i class="fa fa-spinner fa-spin"></i>';
      throughputRate = passedResults.s2cRate;
    } else if (returned_message === 'interval_c2s' && vm.state === 'running_c2s') {
      vm.serverList[vm.iterator].uploadSpeed = '<i class="fa fa-spinner fa-spin"></i>';
      throughputRate = passedResults.c2sRate;
    }
    else {
      // vm.serverList[vm.iterator].latency = '<i class="fa fa-spinner fa-spin"></i>';
      throughputRate = passedResults.MinRTT;
    }

    if (throughputRate !== undefined) {
      vm.update_display(progress_label,
        ((throughputRate / 1000).toFixed(2) + ' ' + $filter('translate')('general.MBPS')));
      if (progress_label.indexOf($filter('translate')('home.test.UPLOAD')) > -1)
      {
        vm.instantUploadSpeed.push([vm.graphIterations, (parseInt(throughputRate / 1000).toFixed(2))]);
        vm.instantDownloadSpeed.push([vm.graphIterations, 0]);
        vm.refreshSpline = !vm.refreshSpline;
        vm.graphIterations++;
      }

      if (progress_label.indexOf($filter('translate')('home.test.DOWNLOAD')) > -1)
      {
        vm.instantDownloadSpeed.push([vm.graphIterations, (parseInt(throughputRate / 1000).toFixed(2))]);
        vm.instantUploadSpeed.push([vm.graphIterations, 0]);
        vm.refreshSpline = !vm.refreshSpline;
        vm.graphIterations++;
      }
    }
  }


  /**
   * Callback function: Starts another test if there is another server in the que or update the display
   * @param passed_results contains all of NDT measurement
   * @TODO: Put a Url here to show all the indices (metric names) available in passed_results
   */
  function onfinish(passed_results) {
    // logger.info("onfinish function: testing number: %s", vm.iterator+1);

    var result_string,
      dy_current,
      metric_name;
    var dy_offset = 1.55;
    var results_to_display = {
      's2cRate': 'Download',
      'c2sRate': 'Upload',
      'MinRTT': 'Latency'
    };

    for (metric_name in results_to_display) {
      if (results_to_display.hasOwnProperty(metric_name) &&
        passed_results.hasOwnProperty(metric_name)) {
        if (metric_name !== 'MinRTT') {
          result_string = Number(passed_results[metric_name] /
            1000).toFixed(2);
          if (!$scope.$$phase) {
            $scope.$apply(function () {
              if (metric_name == 's2cRate') {
                vm.downloadRates.push(result_string);
                vm.serverList[vm.iterator].downloadSpeed = result_string;
                vm.downloadAverage = getAverage(vm.downloadRates);
              } else {
                vm.uploadRates.push(result_string);
                vm.serverList[vm.iterator].uploadSpeed = result_string;
                vm.uploadAverage = getAverage(vm.uploadRates);
              }
            });
          } else {
            if (metric_name == 's2cRate') {
              vm.downloadRates.push(result_string);
              vm.serverList[vm.iterator].downloadSpeed = result_string;
              vm.downloadAverage = getAverage(vm.downloadRates);
            } else {
              vm.uploadRates.push(result_string);
              vm.serverList[vm.iterator].uploadSpeed = result_string;
              vm.uploadAverage = getAverage(vm.uploadRates);
            }
          }
          result_string += $filter('translate')('home.test.MBPS');
        } else {
          result_string = Number(passed_results[metric_name]).toFixed(2);
          vm.latencyRates.push(result_string);
          vm.serverList[vm.iterator].latency = result_string;
          vm.latencyAverage = getAverage(vm.latencyRates);
        }
        vm.update_display(results_to_display[metric_name], result_string);
      }
    }
    // Send the blob data back to the server
    Speedtest.reportPassedResults(passed_results, vm.bindingHash, vm.serverList[vm.iterator].downloadSpeed,
      vm.serverList[vm.iterator].latency, vm.serverList[vm.iterator].uploadSpeed, vm.currentLatitude, vm.currentLongitude).then(function(hash){
      // This is the success promise, updating the value of binding hash. A failure in the function call is silently ignored.
      vm.bindingHash = hash;
      localStorage.setItem('bindingHash', hash);
    });

    // Checks if all the servers have been tested
    if ((vm.iterator + 1) == vm.serverList.length) {
      if (!$scope.$$phase) {
        $scope.$apply(function () {
          vm.showAverage = true;
          vm.testInProgress = false;
          vm.testButtonLabel = $filter('translate')('home.test.TEST_AGAIN');
        });
      }
    } else {
      vm.iterator++;
      Speedtest.startTest(vm.serverList[vm.iterator].url, vm.port, vm.path, vm.callbacks, 1000);
    }
  }

  /**
   * Callback function: In case sth goes wrong show it to the user
   * @param error_message
   */
  function onerror(error_message) {
    // logger.error("onerror: NDT test failed. Test no: %s, Error: %s", vm.iterator+1, error_message);
    d3.timer.flush();
    d3.selectAll('#progress-meter').classed('progress-error', true);
    vm.update_display('Error!', error_message);
    if ((vm.iterator + 1) == vm.serverList.length) {
      if (!$scope.$$phase) {
        $scope.$apply(function () {
          vm.showAverage = true;
          vm.testInProgress = false;
          vm.testButtonLabel = $filter('translate')('home.TEST_AGAIN');
        });
      }
    } else {
      vm.iterator++;
      Speedtest.startTest(vm.serverList[vm.iterator].url, vm.port, vm.path, vm.callbacks, 1000);
    }
  }

}// End of controller
