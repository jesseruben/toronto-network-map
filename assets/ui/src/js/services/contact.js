/**
 * Contact
 * @namespace app.contact.services
 */
(function () {
    'use strict';

    angular
        .module('app')
        .factory('Contact', Contact);

    Contact.$inject = ['$http', '$translate', '$filter', '$log'];

    /**
     * @namespace Contact
     * @returns {Factory}
     */
    function Contact($http, $translate, $filter, $log) {
        /**
         * @name Contact
         * @desc The Factory to be returned
         */
        var Contact = {
            // This is personal preference, but I find it's more readable to define your service
            // as a named object and then return it, we expose this utilises by this method as a part of our service
            sendMessage: sendMessage
        };

        return Contact;

        /**
         * @name sendMessage
         * @desc Try to send a contact message
         * @param {data} An object with several properties listed here
         * @returns {Promise}
         * @memberOf ndtApp.contact.services
         */
        function sendMessage(name, email, subject, message) {
            return $http.post('/contact/', {
                name: name,
                email: email,
                subject: subject,
                message: message
            });
        }

    }
})();
