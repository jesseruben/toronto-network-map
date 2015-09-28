/**
 * AngularJS supports the use of modules. Modularization is a great feature because it promotes encapsulation and loose coupling.
 */

/**
 * Authentication
 * @namespace toolApp.authentication.services
 */
(function () {
    'use strict';

    angular
        .module('ndtApp.authentication.services')
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$cookies', '$http', '$translate', '$filter', 'notify', '$log'];

    /**
     * @namespace Authentication
     * @returns {Factory}
     */
    function Authentication($cookies, $http, $translate, $filter, notify, $log) {
        var logger = $log.getInstance('Authentication Service');
        /**
         * @name Authentication
         * @desc The Factory to be returned
         */
        var Authentication = {
            // This is personal preference, but I find it's more readable to define your service
            // as a named object and then return it, we expose this utilises by this method as a part of our service
            getAuthenticatedAccount: getAuthenticatedAccount,
            isAuthenticated: isAuthenticated,
            login: login,
            logout: logout,
            register: register,
            setAuthenticatedAccount: setAuthenticatedAccount,
            unauthenticate: unauthenticate,
            updatePassword: updatePassword,
            sendForgotPasswordEmail: sendForgotPasswordEmail,
            setPassword: setPassword,
            deactivate: deactivate
        };

        return Authentication;

        ///////////////////

        /**
         * @name getAuthenticatedAccount
         * @desc Return the currently authenticated account
         * @returns {object|undefined} Account if authenticated, else `undefined`
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function getAuthenticatedAccount() {
            if (!$cookies.get('authenticatedAccount')) {
                return;
            }

            return JSON.parse($cookies.get('authenticatedAccount'));
        }

        /**
         * @name getAuthenticatedAccount
         * @desc Return the currently authenticated account
         * @returns {object|undefined} Account if authenticated, else `undefined`
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function deactivate(password) {
            return $http.post('/accounts/deactivate/', {
                password: password
            }).then(deactivateSuccessFn, deactivateErrorFn);

            /**
             * @name deactivateSuccessFn
             * @desc unauthenticates the user, with the success message and returns the user to the home page
             */
            function deactivateSuccessFn(data) {
                Authentication.unauthenticate();
                if (data.data.message && data.data.status){
                    var msg= '<span><strong>' + data.data.status+ ': </strong>' + data.data.message+ '</span>';
                    notify({
                        messageTemplate :msg,
                        duration : '3000',
                        classes : "alert-success"
                    });
                } else {
                    $log.debug('deactivatedSuccessFn: No proper data was returned from the server');
                }
                window.location = '/';
            }

            /**
             * @name deactivateErrorFn
             * @desc Shows a notification with the error
             */
            function deactivateErrorFn(data) {
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


        /**
         * @name isAuthenticated
         * @desc Check if the current user is authenticated
         * @returns {boolean} True if user is authenticated, else false.
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function isAuthenticated() {
            // !! better use to convert a value to boolean
            // angular 1.3 syntax
            //return !!$cookies.authenticatedAccount;
            return !!$cookies.get('authenticatedAccount');
        }


        /**
         * @name login
         * @desc Try to log in with email `email` and password `password`
         * @param {string} email The email entered by the user
         * @param {string} password The password entered by the user
         * @returns {Promise}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function login(email, password) {
            return $http.post('/accounts/login/', {
                email: email, password: password
            }).then(loginSuccessFn, loginErrorFn);

            /**
             * @name loginSuccessFn
             * @desc Set the authenticated account and redirect to index
             */
            function loginSuccessFn(data, status, headers, config) {
                Authentication.setAuthenticatedAccount(data.data.account);
                if (data.data.message && data.data.status){
                    var msg= '<span><strong>' + data.data.status+ ': </strong>' + data.data.message+ '</span>';
                    notify({
                        messageTemplate :msg,
                        duration : '3000',
                        classes : "alert-success"
                    });
                } else {
                    logger.error("Inappropriate data is returned from the server: [%s]:  %s", status, data);
                }
                window.location = '/';
            }

            /**
             * @name loginErrorFn
             * @desc Log "Epic failure!" to the console
             */
            function loginErrorFn(data, status, headers, config) {
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


        /**
         * @name logout
         * @desc Try to log the user out
         * @returns {Promise}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function logout() {
            return $http.post('/accounts/logout/')
                .then(logoutSuccessFn, logoutErrorFn);

            /**
             * @name logoutSuccessFn
             * @desc Unauthenticate and reload the home page
             */
            function logoutSuccessFn(data, status, headers, config) {
                Authentication.unauthenticate();
                if (data.data.message && data.data.status){
                    var msg= '<span><strong>' + data.data.status+ ': </strong>' + data.data.message+ '</span>';
                    notify({
                        messageTemplate :msg,
                        duration : '3000',
                        classes : "alert-success"
                    });
                } else {
                    $log.debug('logoutSuccessFn: No proper data was returned from the server');
                }
                window.location = '/';
            }

            /**
             * @name logoutErrorFn
             * @desc show a notification error
             */
            function logoutErrorFn(data, status, headers, config) {
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


        /**
         * @name register
         * @desc Try to register a new user
         * @param {string} email The email entered by the user
         * @param {string} password The password entered by the user
         * @param {string} confirm_password should be the same as password
         * @param {string} username The username entered by the user
         * @returns {Promise}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function register(email, password, confirm_password, username) {
            return $http.post('/accounts/register/', {
                username: username,
                password: password,
                confirm_password: confirm_password,
                email: email
            }).then(registerSuccessFn, registerErrorFn);

            /**
             * @name registerSuccessFn
             * @desc Log the new user in
             */
            function registerSuccessFn(data, status, headers, config) {
                var msg = '';
                if (data.data.message && data.data.status) {
                    msg = '<span><strong>' + data.data.status + ': </strong>' + data.data.message + '</span>';
                    notify({
                        messageTemplate: msg,
                        duration: '3000',
                        classes: "alert-success"
                    });
                } else {
                    $log.debug('registerSuccessFn: No proper data was returned from the server');
                }
                Authentication.login(email, password);
            }

            /**
             * @name registerErrorFn
             * @desc Log "Epic failure!" to the console
             */
            function registerErrorFn(data, status, headers, config) {
                var msg = '';
                if (data.data.message && data.data.status){
                    msg = '<span><strong>' + data.data.status + ': </strong>' + data.data.message + '</span>';
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

        /**
         * @name setAuthenticatedUser
         * @desc Stringify the account object and store it in a cookie
         * @param {Object} account The acount object to be stored
         * @returns {undefined}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function setAuthenticatedAccount(account) {
            // Angular 1.3 syntax
            //$cookies.authenticatedAccount = JSON.stringify(account);
            $cookies.put('authenticatedAccount', JSON.stringify(account));
        }

        /**
         * @name unauthenticate
         * @desc Delete the cookie where the account object is stored, it's different than logout and it happens at UI
         * @returns {undefined}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function unauthenticate() {
            // angular 1.3 syntax
            // delete $cookies.authenticatedAccount;
            $cookies.remove('authenticatedAccount');
        }

        /**
         * @name updatePassword
         * @desc Try to update password of the user
         * @param {string} user_password The password entered by the user
         * @param {string} new_password The new password entered by the user
         * @param {string} confirm_password The confirmed new password entered by the user
         * @returns {Promise}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function updatePassword(user_password, new_password, confirm_password) {
            return $http.post('/accounts/updatepassword/', {
                password: user_password,
                new_password: new_password,
                confirm_password: confirm_password
            }).then(updatePasswordSuccessFn, updatePasswordErrorFn);

            /**
             * @name updatePasswordSuccessFn
             * @desc Log the updated password in
             */
            function updatePasswordSuccessFn(data, status, headers, config) {
                if (data.data.message && data.data.status) {
                    var msg = '<span><strong>' + data.data.status + ': </strong>' + data.data.message + '</span>';
                    notify({
                        messageTemplate: msg,
                        duration: '3000',
                        classes: "alert-success"
                    });
                } else {
                    $log.debug('updatePasswordSuccessFn: No proper data was returned from the server');
                }
            }

            /**
             * @name updatePasswordErrorFn
             * @desc Show the errors in red below the submit button
             */
            function updatePasswordErrorFn(data, status, headers, config) {
                var msg = '';
                if (data.data.message && data.data.status){
                    msg= '<span><strong>' + data.data.status+ ': </strong>' + data.data.message+ '</span>';
                    notify({
                        messageTemplate :msg,
                        duration : '0',
                        classes : "alert-danger"
                    });
                } else {
                    msg= $filter('translate')('INTERNAL_ERROR');
                    notify({
                        message :msg,
                        duration : '0',
                        classes : "alert-danger"
                    });
                }
            }
        }

        /**
         * @name sendForgotPasswordEmail
         * @desc Gets the users email to send a forgot password message to
         * @param {string} email user's email address to which the forgot password email is sent
         * @returns {Promise}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function sendForgotPasswordEmail(email)
        {
            return $http.post('/accounts/forgotpassword/', {
                email: email
            }).then(forgotPasswordSuccessFn, forgotPasswordErrorFn);

            /**
             * @name forgotPasswordSuccessFn
             * @desc redirect the user to a new page that confirms that an email is sent to him
             */
            function forgotPasswordSuccessFn(data, status, headers, config) {
                if (data.data.message && data.data.status) {
                    var msg = '<span><strong>' + data.data.status + ': </strong>' + data.data.message + '</span>';
                    notify({
                        messageTemplate: msg,
                        duration: '3000',
                        classes: "alert-success"
                    });
                } else {
                    $log.debug('forgotPasswordSuccessFn: No proper data was returned from the server');
                }
            }

            /**
             * @name forgotPasswordErrorFn
             * @desc Show the errors in red below the submit button
             */
            function forgotPasswordErrorFn(data, status, headers, config) {
                var msg = '';
                if (data.data.message && data.data.status){
                    msg= '<span><strong>' + data.data.status+ ': </strong>' + data.data.message+ '</span>';
                    notify({
                        messageTemplate :msg,
                        duration : '0',
                        classes : "alert-danger"
                    });
                } else {
                    msg = $filter('translate')('INTERNAL_ERROR');
                    notify({
                        message: msg,
                        duration: '0',
                        classes: "alert-danger"
                    });
                }
            }
        }

        /**
         * @name setPassword
         * @desc Gets the new password and confirm password and pass them over to the backend server
         * @param {string} guid is sting of unique identifier for activation
         * @param {string} new_password user's new password
         * @param {string} confirm_password confirmation of the new password
         * @returns {Promise}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function setPassword(guid, new_password, confirm_password)
        {
            return $http.post('/accounts/setpassword/', {
                guid: guid,
                new_password: new_password,
                confirm_password: confirm_password
            }).then(setPasswordSuccessFn, setPasswordErrorFn);

            /**
             * @name setPasswordSuccessFn
             * @desc Confirm that the new password is set
             */
            function setPasswordSuccessFn(data, status, headers, config) {
                var msg = '';
                if (data.data.message && data.data.status) {
                    msg = '<span><strong>' + data.data.status + ': </strong>' + data.data.message + '</span>';
                    notify({
                        messageTemplate: msg,
                        duration: '3000',
                        classes: "alert-success"
                    });
                } else {
                    $log.debug('setPasswordSuccessFn: No proper data was returned from the server');
                }
                window.location = "/login";

            }

            /**
             * @name setPasswordErrorFn
             * @desc Show the errors in red below the submit button
             */
            function setPasswordErrorFn(data, status, headers, config) {
                var msg = '';
                if (data.data.message && data.data.status){
                    msg= '<span><strong>' + data.data.status+ ': </strong>' + data.data.message+ '</span>';
                    notify({
                        messageTemplate :msg,
                        duration : '0',
                        classes : "alert-danger"
                    });
                } else {
                    msg = $filter('translate')('INTERNAL_ERROR');
                    notify({
                        message: msg,
                        duration: '0',
                        classes: "alert-danger"
                    });
                }
            }
        }

    }
})();
