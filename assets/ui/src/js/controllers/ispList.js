/**
 * IspListController
 * @namespace app.controllers
 */
(function () {
    'use static';

    angular
        .module('app')
        .controller('IspListController', IspListController);

    IspListController.$inject = ['$log', 'Isp', '$filter'];

    /**
     * @namespace IspListController
     */
    function IspListController($log, Isp, $filter) {
        var vm = this;
        logger = $log.getInstance('IspListController');

        vm.getIsps = getIsps;
        vm.isps = null;
        vm.orderOptions = [
          {
              name : 'AZ',
              value : 'name'
          },
          {
              name : 'ZA',
              value : '-name'
          },
            {
                name : $filter('translate')('ispList.HIGHEST_RATING'),
                value : 'rating'
            },
            {
              name : $filter('translate')('ispList.LOWEST_RATING'),
              value : '-rating'
            }
        ];


        activate();

        function activate(){
            return getIsps().then(function() {
               logger.info('Activated Isps list view')
            });
        }

        /**
         * Get a list of ISPS from service
         */
        function getIsps(){
            return Isp.list().then(listSuccessFn).catch(listErrorFn);

            function listSuccessFn(data){
                logger.debug(data);
                vm.isps = data.data;
                return vm.isps;
            }

            function listErrorFn(){
                logger.warn('Could not get list of isps from the service');
            }
        }

    }
})();