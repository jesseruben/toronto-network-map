module.exports = function() {
  var client = './';
  var build = './build/';

  var config = {

      // All the js files we want to vet
      alljs: [
         client + 'app/bower_components/jquery/dist/jquery.js',
         client + 'app/bower_components/bootstrap/dist/js/bootstrap.js',
         client + 'app/bower_components/angular/angular.js',
         client + 'app/bower_components/d3/d3.js',
         client + 'app/bower_components/angular-animate/angular-animate.js',
         client + 'app/bower_components/angular-aria/angular-aria.js',
         client + 'app/bower_components/angular-cookies/angular-cookies.js',
         client + 'app/bower_components/angular-messages/angular-messages.js',
         client + 'app/bower_components/angular-resource/angular-resource.js',
         client + 'app/bower_components/angular-sanitize/angular-sanitize.js',
         client + 'app/bower_components/angular-touch/angular-touch.js',
         client + 'app/bower_components/angular-ui-router/release/angular-ui-router.js',
         client + 'app/bower_components/ngstorage/ngStorage.js',
         client + 'app/bower_components/angular-ui-utils/ui-utils.js',
         client + 'app/bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
         client + 'app/bower_components/angular-translate/angular-translate.js',
         client + 'app/bower_components/angular-translate-loader-static-files/angular-translate-loader-static-files.js',
         client + 'app/bower_components/angular-translate-storage-cookie/angular-translate-storage-cookie.js',
         client + 'app/bower_components/angular-translate-storage-local/angular-translate-storage-local.js',
         client + 'app/bower_components/oclazyload/dist/ocLazyLoad.js',
         client + 'app/bower_components/angular-simple-logger/dist/angular-simple-logger.min.js',
         client + 'app/bower_components/lodash/lodash.min.js',
         client + 'app/bower_components/angular-google-maps/dist/angular-google-maps.min.js',
         client + 'app/bower_components/moment/moment.js',
         client + 'app/bower_components/sprintf/dist/sprintf.min.js',
         client + 'app/bower_components/angular-logger/dist/angular-logger.js',
         client + 'app/bower_components/angularjs-toaster/toaster.js',
         client + 'app/bower_components/jquery-ui/ui/minified/jquery-ui.min.js',
         client + 'app/bower_components/angular-ui-slider/src/slider.js',
         client + 'app/bower_components/c3/c3.js',
         client + 'app/bower_components/bootstrap-select/dist/js/bootstrap-select.js',
         client + 'app/bower_components/angucomplete-alt/angucomplete-alt.js',
         client + 'app/bower_components/angularjs-dropdown-multiselect/dist/angularjs-dropdown-multiselect.min.js',
         client + 'app/bower_components/persianjs/persian.js',
         client + 'app/bower_components/angular-persian/dist/angularpersian.js',
         client + 'src/js/app.js',
         client + 'src/js/main.js',
         client + 'src/js/config.js',
         client + 'src/js/config.router.js',
         client + 'src/js/config.lazyload.js',
         client + 'src/js/constants.js',
         client + 'src/js/*/*.js'
      ],
      ltrcss: [
         client + 'libs/assets/animate.css/animate.css',
         client + 'libs/assets/simple-line-icons/css/simple-line-icons.css',
         client + 'app/bower_components/bootstrap/dist/css/bootstrap.css',
         client + 'app/bower_components/font-awesome/css/font-awesome.css',
         client + 'app/bower_components/angularjs-toaster/toaster.css',
         client + 'app/bower_components/jquery-ui/themes/base/jquery-ui.css',
         client + 'app/bower_components/c3/c3.css',
         client + 'app/bower_components/bootstrap-select/dist/css/bootstrap-select.css',
         client + 'app/bower_components/angucomplete-alt/angucomplete-alt.css',
         client + 'src/css/font.css',
         client + 'src/css/fonts.css',
         client + 'src/css/app.css'
      ],
      rtlcss: [
         client + 'libs/assets/animate.css/animate.css',
         client + 'libs/assets/simple-line-icons/css/simple-line-icons.css',
         client + 'app/bower_components/bootstrap/dist/css/bootstrap.css',
         client + 'app/bower_components/bootstrap-rtl/dist/css/bootstrap-rtl.css',
         client + 'app/bower_components/font-awesome/css/font-awesome.css',
         client + 'app/bower_components/angularjs-toaster/toaster.css',
         client + 'app/bower_components/jquery-ui/themes/base/jquery-ui.css',
         client + 'app/bower_components/c3/c3.css',
         client + 'app/bower_components/bootstrap-select/dist/css/bootstrap-select.css',
         client + 'app/bower_components/angucomplete-alt/angucomplete-alt.css',
         client + 'src/css/font.css',
         client + 'src/css/fonts.css',
         client + 'src/css/app.css',
         client + 'src/css/app.rtl.css'
      ],
      fonts: [
          client + 'app/bower_components/font-awesome/fonts/**/*.*',
          client + 'libs/assets/simple-line-icons/fonts/*.*',
          client + 'src/fonts/*/*.*',
          client + 'src/fonts/*.*'
      ],
      build: build,
      images: client + 'src/img/*.*',
      cssImages: client + 'app/bower_components/jquery-ui/themes/base/images/*.*',
      rtlcssdist: build + 'css/',
      ltrcssdist: build + 'css/',
      staticdata: client + 'staticdata/*.json',
      templates: [
          client + 'src/tpl/*.html',
          client + 'src/tpl/*/*.html'
      ]
  };

  return config;
};
