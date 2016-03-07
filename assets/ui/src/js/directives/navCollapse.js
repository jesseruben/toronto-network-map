// Just add nav-collapse="" to  <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1" nav-collapse="">
angular.module('app').directive('navCollapse', function () {
  return {
    restrict: 'A',
    link: function (scope, element, attrs) {
      var visible = false;

      element.on('show.bs.collapse', function () {
        visible = true;
      });

      element.on("hide.bs.collapse", function () {
        visible = false;
      });

      element.on('click', function (event) {
        if (visible && 'auto' == element.css('overflow-y') && $(event.target).attr('data-toggle') != "dropdown") {
          element.collapse('hide');
        }
      });
    }
  }
});
