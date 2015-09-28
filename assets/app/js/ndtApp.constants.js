(function () {
  'use strict';

    var config_data = {
      'PATH': {
        'BASE_TEMPLATE_URL': 'static/templates/'
      }
    };

    angular.forEach(config_data, function(key, value) {
      angular.module('ndtApp.constants').constant(value, key);
    });

})();







