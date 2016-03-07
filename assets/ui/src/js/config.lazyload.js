// lazyload config

angular.module('app')
    /**
   * jQuery plugin config use ui-jq directive , config the js and css files that required
   * key: function name of the jQuery plugin
   * value: array of the css js file located
   */
  .constant('JQ_CONFIG', {
      sparkline:      [   'static/libs/jquery/jquery.sparkline/dist/jquery.sparkline.retina.js'],
      plot:           [   'static/libs/jquery/flot/jquery.flot.js',
                          'static/libs/jquery/flot/jquery.flot.pie.js',
                          'static/libs/jquery/flot/jquery.flot.resize.js',
                          'static/libs/jquery/flot.tooltip/js/jquery.flot.tooltip.min.js',
                          'static/libs/jquery/flot.orderbars/js/jquery.flot.orderBars.js',
                          'static/app/bower_components/flot-axislabels/jquery.flot.axislabels.js',
                          'static/app/bower_components/flot/jquery.flot.time.js',
                          'static/libs/jquery/flot-spline/js/jquery.flot.spline.min.js'],
     screenfull:      [   'static/libs/jquery/screenfull/dist/screenfull.min.js']
    }
  )
  .constant('MODULE_CONFIG', [
      {
          name: 'ngGrid',
          files: [
              'static/libs/angular/ng-grid/build/ng-grid.min.js',
              'static/libs/angular/ng-grid/ng-grid.min.css',
              'static/libs/angular/ng-grid/ng-grid.bootstrap.css'
          ]
      }
    ]
  )
  // oclazyload config
  .config(['$ocLazyLoadProvider', 'MODULE_CONFIG', function($ocLazyLoadProvider, MODULE_CONFIG) {
      // We configure ocLazyLoad to use the lib script.js as the async loader
      $ocLazyLoadProvider.config({
          debug:  false,
          events: true,
          modules: MODULE_CONFIG
      });
  }])
;
