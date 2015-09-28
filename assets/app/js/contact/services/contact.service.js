/**
 * Report
 * @namespace ndtApp.contact.services
 */
(function () {
  'use strict';

  angular
    .module('ndtApp.contact.services')
    .factory('Contact', Contact);

  Contact.$inject = ['$http', '$translate', '$filter', 'notify', '$log'];

  /**
   * @namespace Contact
   * @returns {Factory}
   */
  function Contact($http, $translate, $filter, notify, $log) {
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
    function sendMessage(email, subject, message) {
      return $http.post('/contact/', {
        email: email,
        subject: subject,
        message: message
      }).then(sendMessageSuccessFn, sendMessageErrorFn);

      /**
       * @name sendMessageSuccessFn
       * @desc shows the success message
       */
      function sendMessageSuccessFn(data) {
        if (data.data.message && data.data.status){
          var msg= '<span><strong>' + data.data.status+ ': </strong>' + data.data.message+ '</span>';
            notify({
                messageTemplate :msg,
                duration : '3000',
                classes : "alert-success"
            });
        } else {
          $log.debug('sendMessageSuccessFn: No proper data was returned from the server');
        }
        window.location = '/';
      }

      /**
       * @name sendMessageErrorFn
       * @desc Shows a notification with the error
       */
      function sendMessageErrorFn(data) {
          var msg = '';
          if (data.data.message && data.data.status){
                msg = '<span><strong>' + data.data.status+ ': </strong>' + data.data.message+ '</span>';
                notify({
                    messageTemplate :msg,
                    duration : '0',
                    classes : "alert-danger"
                });
          } else {
                 msg = $filter('translate')('INTERNAL_ERROR');
                 notify({
                    message :msg,
                    duration : '0',
                    classes : "alert-danger"
                });
          }
      }
    }

  }
})();
