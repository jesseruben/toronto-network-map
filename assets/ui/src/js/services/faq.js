/**
 * Faq
 * @namespace app.faq.services
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('Faq', Faq);

    Faq.$inject = ['$http'];

    /**
     * @namespace Faq
     * @returns {Factory}
     */
    function Faq($http) {
        /**
         * @name Contact
         * @desc The Factory to be returned
         */
        var Faq = {
            getFaqs: getFaqs
        };

        return Faq;

        /**
         * @name getFaqs
         * @desc get the list of FAQa
         * @returns {Promise}
         * @memberOf app.faq.services
         */
        function getFaqs() {
            return $http.get('/faq/');
        }

    }
})();
