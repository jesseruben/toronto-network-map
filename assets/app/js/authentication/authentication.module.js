(function () {
  'use strict';

    // This the module we're going to inject in other places and it encompass both the controller
    // and the services
  angular
    .module('ndtApp.authentication', [
      'ndtApp.authentication.controllers',
      'ndtApp.authentication.services',
      'ndtApp.authentication.directives'
    ]);

  angular
    .module('ndtApp.authentication.controllers', []);

  angular
    .module('ndtApp.authentication.services', ['ngCookies']);

  angular
    .module('ndtApp.authentication.directives', []);

})();