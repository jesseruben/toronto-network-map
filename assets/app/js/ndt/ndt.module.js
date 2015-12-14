(function () {
  'use strict';

  angular
    .module('ndtApp.ndt', [
      'ndtApp.ndt.controllers',
       'ndtApp.ndt.filters',
      'ndtApp.ndt.services'
    ]);

  angular
    .module('ndtApp.ndt.controllers', []);

  angular
      .module('ndtApp.ndt.services', []);

  angular
    .module('ndtApp.ndt.filters', []);

})();