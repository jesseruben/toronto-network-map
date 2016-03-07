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
        .module('Authentication', [])
        .factory('Authentication', Authentication);

    Authentication.$inject = ['$http', '$translate', '$filter', 'toaster', '$log', '$q', 'AUTH_EVENTS',
        '$rootScope', 'USER_ROLES', '$uibModal'];

    /**
     * @namespace Authentication
     * @returns {Factory}
     */
    function Authentication($http, $translate, $filter, toaster, $log, $q, AUTH_EVENTS
        , $rootScope, USER_ROLES, $uibModal) {
        var logger = $log.getInstance('Authentication Service');
        /**
         * @name Authentication
         * @desc The Factory to be returned
         */
        var Authentication = {
            getAuthenticatedAccount: getAuthenticatedAccount,
            isAuthenticated: isAuthenticated,
            isAuthorized: isAuthorized,
            login: login,
            logout: logout,
            register: register,
            setAuthenticatedAccount: setAuthenticatedAccount,
            unauthenticate: unauthenticate,
            updatePassword: updatePassword,
            sendForgotPasswordEmail: sendForgotPasswordEmail,
            setPassword: setPassword,
            launchModal: launchModal,
            deactivate: deactivate
        };

        return Authentication;

        ///////////////////
        function launchModal(tab) {
            logger.info(tab);
            var instance =$uibModal.open({
                templateUrl: 'static/src/tpl/page_signin.html',
                controller: 'LoginModalCtrl',
                controllerAs: 'vm',
                resolve: {
                    tab: function (){
                    return tab;
                    }
                }
            });

            return instance.result.then();
        }

        /**
         * @name getAuthenticatedAccount
         * @desc Return the currently authenticated account
         * @returns {object|undefined} Account if authenticated, else `undefined`
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function getAuthenticatedAccount() {
            if (localStorage.authenticatedAccount) {
                return JSON.parse(localStorage.authenticatedAccount);
            } else {
                return null;
            }
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
                    toaster.pop('success', $filter('translate')('errors.SUCCESS'), $filter('translate')('errors.' + data.data.message));
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
                    toaster.pop('warning', $filter('translate')('errors.SUCCESS'), $filter('translate')('errors.' + data.data.message));
                } else {
                    msg = $filter('translate')('INTERNAL_SERVER_ERROR');
                    toaster.pop('warning', 'Authentication',msg)
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
            return !!localStorage.authenticatedAccount;
        }


        function isAuthorized (authorizedRoles) {
            if (!angular.isArray(authorizedRoles)) {
              authorizedRoles = [authorizedRoles];
            }
            if (authorizedRoles.indexOf(USER_ROLES.all) !== -1){
                // everyone can have access to that view
                return true;
            } else {
                // check if the localStorage.userRole is index of authorizedRoles array coming from router
                // for now we replace this with all authenticated users
                // return (authorizedRoles.indexOf(localStorage.userRole) !== -1);
                return Authentication.isAuthenticated();
            }
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
            logger.info('login was called with'+email+password);
            return $http.post('/accounts/login/', {
                email: email, password: password
            }).then(loginSuccessFn, loginErrorFn);

            /**
             * @name loginSuccessFn
             * @desc Set the authenticated account and redirect to index
             */
            function loginSuccessFn(data, status, headers, config) {
                logger.info('loginSuccessFn was called');
                Authentication.setAuthenticatedAccount(data.data.account);
                if (data.data.message && data.data.status){
                    toaster.pop('success', $filter('translate')('errors.SUCCESS'), $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                    $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
                } else {
                    $rootScope.$broadcast(AUTH_EVENTS.loginFail);
                    logger.error("Inappropriate data is returned from the server: [%s]:  %s", status, data);
                }
                return data.data;
            }

            /**
             * @name loginErrorFn
             * @desc Log "Epic failure!" to the console
             */
            function loginErrorFn(data, status, headers, config) {
                $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
                // Note that if we return a non-promised value from the error callback it will
                // resolve and not reject the derived promise. So we need to reject it explicitly.
                return $q.reject(data.data);
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
                    toaster.pop('success', $filter('translate')('errors.SUCCESS'), $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                } else {
                    $log.debug('logoutSuccessFn: No proper data was returned from the server');
                }
                return data.data;

            }

            /**
             * @name logoutErrorFn
             * @desc show a notification error
             */
            function logoutErrorFn(data, status, headers, config) {
                if (data.data.message && data.data.status){
                    toaster.pop('warning', $filter('translate')('errors.WARNING') , $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                } else {
                    toaster.pop('warning', $filter('translate')('errors.WARNING'), $filter('translate')('errors.INTERNAL_SERVER_ERROR'), 5000, 'trustedHtml');
                }
                return $q.reject(data.data);
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
            logger.info('register is called'+email+password+confirm_password+username);
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
                if (data.data.message && data.data.status) {
                    logger.info('register service was successful'+data.data.message);
                    toaster.pop('success', $filter('translate')('errors.SUCCESS') , $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                    return Authentication.login(email, password);
                } else {
                    $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
                    $log.debug('registerSuccessFn: No proper data was returned from the server');
                }
            }

            /**
             * @name registerErrorFn
             * @desc Log "Epic failure!" to the console
             */
            function registerErrorFn(data, status, headers, config) {
                logger.error('regiser unsuccessful ' + data.data.message);
                $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
                return $q.reject(data.data);
            }
        }

        /**
         * @name setAuthenticatedUser
         * @desc Stringify the account object and store it in a localStorage
         * @param {Object} account The acount object to be stored
         * @returns {undefined}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function setAuthenticatedAccount(account) {
            localStorage.setItem('authenticatedAccount', JSON.stringify(account));
        }

        /**
         * @name unauthenticate
         * @desc Delete the localStorage where the account object is stored, it's different than logout and it happens at UI
         * @returns {undefined}
         * @memberOf ndtApp.authentication.services.Authentication
         */
        function unauthenticate() {
            localStorage.removeItem('authenticatedAccount');
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
                    toaster.pop('success', $filter('translate')('errors.SUCCESS') , $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                } else {
                    $log.debug('updatePasswordSuccessFn: No proper data was returned from the server');
                }
            }

            /**
             * @name updatePasswordErrorFn
             * @desc Show the errors in red below the submit button
             */
            function updatePasswordErrorFn(data, status, headers, config) {
                if (data.data.message && data.data.status){
                    toaster.pop('warning', $filter('translate')('errors.WARNING') , $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                } else {
                    toaster.pop('warning', $filter('translate')('errors.WARNING') , $filter('translate')('errors.INTERNAL_SERVER_ERROR'), 5000, 'trustedHtml');
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
                    toaster.pop('success', $filter('translate')('errors.SUCCESS') , $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                } else {
                    $log.debug('forgotPasswordSuccessFn: No proper data was returned from the server');
                }
            }

            /**
             * @name forgotPasswordErrorFn
             * @desc Show the errors in red below the submit button
             */
            function forgotPasswordErrorFn(data, status, headers, config) {
                if (data.data.message && data.data.status){
                    toaster.pop('warning', $filter('translate')('errors.WARNING') , $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                } else {
                    toaster.pop('warning', 'Authentication' , $filter('translate')('errors.INTERNAL_SERVER_ERROR'), 5000, 'trustedHtml');
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
                if (data.data.message && data.data.status) {
                    toaster.pop('warning', $filter('translate')('errors.SUCCESS') , $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                } else {
                    $log.debug('setPasswordSuccessFn: No proper data was returned from the server');
                }
            }

            /**
             * @name setPasswordErrorFn
             * @desc Show the errors in red below the submit button
             */
            function setPasswordErrorFn(data, status, headers, config) {
                if (data.data.message && data.data.status){
                    toaster.pop('warning', $filter('translate')('WARNING'), $filter('translate')('errors.' + data.data.message), 5000, 'trustedHtml');
                } else {
                    toaster.pop('warning', $filter('translate')('WARNING') , $filter('translate')('errors.INTERNAL_SERVER_ERROR'), 5000, 'trustedHtml');
                }
            }
        }

    }
})();
