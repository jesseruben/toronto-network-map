(function () {
    'use static';

    angular
        .module('ndtApp')
        .directive('pwCheck', pwCheck)
        .directive('validAlphaNumeric', validAlphaNumeric)
        .directive('validEmail', validEmail);

    function pwCheck() {
        return {
            require: 'ngModel',
            link: function (scope, elem, attrs, ctrl) {
                var firstPassword = '#' + attrs.pwCheck;
                elem.add(firstPassword).on('keyup', function () {
                    scope.$apply(function () {
                        var v = elem.val() === $(firstPassword).val();
                        ctrl.$setValidity('pwmatch', v);
                    });
                });
            }
        }
    }

    function validEmail() {
        return {
             require: 'ngModel',
             link: function(scope, elm, attrs, ctrl){
                 var validator = function(value){
                     if (value == '' || typeof value == 'undefined') {
                         ctrl.$setValidity('validEmail', true);
                     } else {
                         var emailRegex = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
                         ctrl.$setValidity('validEmail', emailRegex.test(value));
                     }
                     return value;
                 };

                 // replace all other validators!
                 ctrl.$parsers = [validator];
                 ctrl.$formatters = [validator];
             }
         }
     }

    function validAlphaNumeric() {
        return {
            require: 'ngModel',
            restrict: 'A',
            link: function(scope, elem, attr, ngModel) {
                var validator = function(value) {
                   if (/^[a-zA-Z0-9]*$/.test(value)) {
                        ngModel.$setValidity('alphanumeric', true);
                        return value;
                   } else {
                       ngModel.$setValidity('alphanumeric', false);
                       return undefined;
                   }
                };
                ngModel.$parsers.unshift(validator);
                ngModel.$formatters.unshift(validator);
            }
        };
    }

})();