
(function () {
    'use strict';

    angular
        .module('loginModal', [])
        .factory('loginModal', loginModal);

    loginModal.$inject = ['$uibModal', '$rootScope'];


    function loginModal($uibModal, $rootScope) {

        var loginModal ={
            assignCurrentUser:assignCurrentUser,
            launchModal: launchModal,
        };
        return loginModal;

        function assignCurrentUser (user) {
            $rootScope.currentUser = user;
            return user;
        }

        function launchModal() {
            var instance = $uibModal.open({
                templateUrl: 'static/src/tpl/page_signin.html',
                controller: 'LoginModalCtrl',
                controllerAs: 'vm'
            });

            return instance.result.then(assignCurrentUser);
        }

    }
})();
