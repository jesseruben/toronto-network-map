// Karma configuration
// Generated on Tue Oct 27 2015 11:55:55 GMT-0400 (EDT)

module.exports = function(config) {
  config.set({

    // base path that will be used to resolve all patterns (eg. files, exclude)
    basePath: '',


    // frameworks to use
    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
    frameworks: ['jasmine'],


    // list of files / patterns to load in the browser
    files: [
      'app/bower_components/jquery/dist/jquery.js',
      'app/bower_components/angular/angular.js',
      'app/bower_components/bootstrap/dist/js/bootstrap.js',
      'app/bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
      'app/bower_components/angular-animate/angular-animate.js',
      'app/bower_components/angular-cookies/angular-cookies.js',
      'app/bower_components/angular-translate/angular-translate.js',
      'app/bower_components/angular-translate-storage-cookie/angular-translate-storage-cookie.js',
      'app/bower_components/angular-messages/angular-messages.js',
      'app/bower_components/angular-resource/angular-resource.js',     
      'app/bower_components/angular-route/angular-route.js',
      'app/bower_components/angular-sanitize/angular-sanitize.js',
      'app/bower_components/angular-touch/angular-touch.js',
      'app/bower_components/angular-notify/dist/angular-notify.js',
      'app/bower_components/sprintf/dist/sprintf.min.js',
      'app/bower_components/moment/moment.js',
      'app/bower_components/angular-logger/dist/angular-logger.js',
      'app/bower_components/d3/d3.js',
      'app/bower_components/angular-simple-logger/dist/angular-simple-logger.min.js',
      'app/bower_components/lodash/lodash.min.js',
      'app/bower_components/angular-google-maps/dist/angular-google-maps.min.js',
      'app/bower_components/angular-material/angular-material.js',
      'app/bower_components/angular-aria/angular-aria.js',
      'app/bower_components/angular-ui-slider/src/slider.js',
      'node_modules/angular-mocks/angular-mocks.js',
      'app/js/ndtApp.js',
      'app/js/ndtApp.constants.js',
      'app/js/ndtApp.routes.js',
      'app/js/ndtApp.config.js',
      'app/js/static/static.module.js',
      'app/js/*/*.js',
      'app/js/*/*/*.js',
      'test/spec/*/*.js'
    ],


    // list of files to exclude
    exclude: [
    ],


    // preprocess matching files before serving them to the browser
    // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
    preprocessors: {
    },


    // test results reporter to use
    // possible values: 'dots', 'progress'
    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
    reporters: ['progress'],


    // web server port
    port: 9876,


    // enable / disable colors in the output (reporters and logs)
    colors: true,


    // level of logging
    // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
    logLevel: config.LOG_INFO,


    // enable / disable watching file and executing tests whenever any file changes
    autoWatch: true,


    // start these browsers
    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
    browsers: ['PhantomJS'],


    // Continuous Integration mode
    // if true, Karma captures browsers, runs the tests and exits
    singleRun: false,

    // Concurrency level
    // how many browser should be started simultanous
    concurrency: Infinity
  })
}
