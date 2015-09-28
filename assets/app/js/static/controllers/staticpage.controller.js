/**
 * Static controller: loads static pages from templates
 * @namespace ndtApp.static.controllers
 */

(function () {
    'use strict';

    angular
        .module('ndtApp.static.controllers')
        .controller('StaticPageController', StaticPageController);


    StaticPageController.$inject =['$translate', '$window']
    /**
     * this is a dummy controller function to load static pages
     * @namespace StaticPageController
     */
    function StaticPageController ($translate, $window) {
        var vm = this;
        // set the language button label the opposite language that system uses
        vm.lang = ($translate.use()=="en") ? "en" : "en";
        vm.changeLanguage = function (langKey) {
                var date = new Date();
                var cookieExpiresInDays = 30;
                date.setTime(date.getTime()+(cookieExpiresInDays*24*60*60*1000));
                var expires = "; expires="+date.toGMTString();

               // $translate.use(langKey);
                if (langKey=='en'){
                    // TODO: put LANG in central config file
                    document.cookie='LANG="en"; path=/' + expires;
                    $window.location.reload();
                } else {
                    document.cookie='LANG="en"; path=/' + expires;
                    $window.location.reload();
                }
        }
    }

})();
