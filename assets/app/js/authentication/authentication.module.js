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
//this one define the controllers only
  angular
    .module('ndtApp.authentication.controllers', []);
//this one defines the services only

  angular
    .module('ndtApp.authentication.services', ['ngCookies']);

  angular
    .module('ndtApp.authentication.directives', []);

})();