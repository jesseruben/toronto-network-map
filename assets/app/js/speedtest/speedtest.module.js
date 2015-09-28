(function () {
  'use strict';

    // This the module we're going to inject in other places and it encompass both the controller
    // and the services
  angular
    .module('ndtApp.speedtest', [
      'ndtApp.speedtest.controllers',
      'ndtApp.speedtest.services'
    ]);

  angular
    .module('ndtApp.speedtest.controllers', []);

  angular
    .module('ndtApp.speedtest.services', []);

})();