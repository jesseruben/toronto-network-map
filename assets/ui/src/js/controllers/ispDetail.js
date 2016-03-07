/**
 * IspDetailController
 * @namespace app.controllers
 */
(function () {
    'use static';

    angular
        .module('app')
        .controller('IspDetailController', IspDetailController);

    IspDetailController.$inject = ['$stateParams', '$filter', '$log', 'Isp'];

    /**
     * @namespace IspDetailController
     */
    function IspDetailController($stateParams,  $filter, $log, Isp) {
        var vm = this;
        logger = $log.getInstance('IspDetailController');

        vm.getIsp = getIsp;
        vm.isp = null;
        vm.tests = null; // latest 5 tests of for this isp


        activate();

        function activate(){
            var id = $stateParams.id;
            return getIsp(id).then(function(data) {
                vm.isp = data.data.isp;
                vm.tests = data.data.tests;
               logger.info('Activated Isps detail view')
            });
        }

        /**
         * Get a single isp with given id (from url) from service
         */
        function getIsp(id){
            return Isp.get(id).then(getSuccessFn).catch(getErrorFn);

            function getSuccessFn(data){
                logger.debug(data);
                return data;
            }

            function getErrorFn(){
                logger.warn('Could not get the single isp from the service');
            }
        }

    }
})();