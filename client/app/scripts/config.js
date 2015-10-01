/**
 * INSPINIA - Responsive Admin Theme
 *
 * Inspinia theme use AngularUI Router to manage routing and views
 * Each view are defined as state.
 * Initial there are written stat for all view in theme.
 *
 */
function config($stateProvider, $urlRouterProvider, $ocLazyLoadProvider) {

    $urlRouterProvider.otherwise("/admin/explorer");

    $ocLazyLoadProvider.config({
        // Set to true if you want to see what and when is dynamically loaded
        debug: true
    });
    

    $stateProvider

        .state('index', {
            abstract: true,
            url: "/index",
            templateUrl: "views/common/content.html",
        })
        .state('index.main', {
            url: "/main",
            templateUrl: "views/main.html",
            data: { pageTitle: 'Example view' }
        })
        .state('index.minor', {
            url: "/minor",
            templateUrl: "views/minor.html",
            data: { pageTitle: 'Example view' }
        })

        .state('admin', {
            abstract: true,
            url: "/admin",
            templateUrl: "views/admin/common/content.html",
        })
        .state('admin.tour', {
            url: "/tour",
            templateUrl: "views/admin/tour.html",
            data: { pageTitle: 'Tour Guiado' }
        })
        .state('admin.explorer', {
            url: "/explorer",
            templateUrl: "views/admin/explorer.html",
            data: { pageTitle: 'Data Explorer' },
            resolve: {
                loadPlugin: function ($ocLazyLoad) {
                    return $ocLazyLoad.load([
                        {
                            serie: true,
                            files: ['bower_components/datatables/media/js/jquery.dataTables.min.js','bower_components/angular-datatables/dist/datatables.bootstrap.min.css']
                        },
                        {
                            serie: true,
                            files: ['bower_components/datatables/media/js/dataTables.bootstrap.min.js']
                        },
                        {
                            name: 'datatables',
                            files: ['bower_components/angular-datatables/dist/angular-datatables.min.js']
                        }
                    ]);
                }
            }
        })
}
angular
    .module('DATAPROJECT')
    .config(config)
    .run(function($rootScope, $state) {
        $rootScope.$state = $state;
    });