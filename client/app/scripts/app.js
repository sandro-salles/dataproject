'use strict';

/**
 * @ngdoc overview
 * @name CONTACTPRO
 * @description
 * # CONTACTPRO
 *
 * Main module of the application.
 */

/*jshint -W079 */

var app = angular
    .module('CONTACTPRO', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngSanitize',
        'ngTouch',
        'ngMessages',
        'picardy.fontawesome',
        'ui.bootstrap',
        'ui.router',
        'ui.utils',
        'angular-loading-bar',
        'angular-momentjs',
        'jcs-autoValidate',
        'FBAngular',
        'toastr',
        'angularBootstrapNavTree',
        'oc.lazyLoad',
        'ui.select',
        'ui.tree',
        'ui.gravatar',
        'textAngular',
        'angular-flot',
        'angular-rickshaw',
        'easypiechart',
        'ui.calendar',
        'ngTagsInput',
        'ngMaterial',
        'localytics.directives',
        'angular-intro',
        'dragularModule',
        'djangoRESTResources',
        'angular-jwt',
        'ngCpfCnpj',
        'dynamicNumber'
    ])
    .run(['$rootScope', '$state', '$stateParams', '$location', '$cookieStore', '$http', 'jwtHelper', 'bootstrap3ElementModifier', 'AuthService', function($rootScope, $state, $stateParams, $location, $cookieStore, $http, jwtHelper, bootstrap3ElementModifier, AuthService) {

        bootstrap3ElementModifier.enableValidationStateIcons(true);

        $rootScope.globals = $cookieStore.get('globals') || {};

        if ($rootScope.globals.currentUser) {
            $http.defaults.headers.common['Authorization'] = 'JWT ' + $rootScope.globals.currentUser.token; // jshint ignore:line
        }

        $rootScope.$state = $state;
        $rootScope.$stateParams = $stateParams;
        $rootScope.$on('$stateChangeSuccess', function(event, toState) {

            event.targetScope.$watch('$viewContentLoaded', function() {

                angular.element('html, body, #content').animate({
                    scrollTop: 0
                }, 200);

                setTimeout(function() {
                    angular.element('#wrap').css('visibility', 'visible');

                    if (!angular.element('.dropdown').hasClass('open')) {
                        angular.element('.dropdown').find('>ul').slideUp();
                    }
                }, 200);
            });
            $rootScope.containerClass = toState.containerClass;
        });

        var checkUserSession = function(next, current) {

            var public_states = ['/core/login/', '/core/forgotpass/', '/core/forgotpass/success/'];
            var restricted = true;
            var current_path = $location.path();
            
            for (var pstate in public_states) {
                if (current_path.indexOf(public_states[pstate]) > -1) {
                    restricted = false;
                    break;
                }
            }

            var loggedIn = $rootScope.globals.currentUser;
            if (restricted && (!loggedIn || jwtHelper.isTokenExpired(loggedIn.token))) {
                
                AuthService.ClearCredentials();

                if (current_path) {
                    $location.path('/core/login/').search('origin', encodeURIComponent(current_path));    
                } else {
                    $location.path('/core/login/');
                }
                
            }
        };

        $rootScope.$on('$locationChangeStart', function(event, next, current) {
            checkUserSession(next, current);
        });

        $rootScope.$on('$stateChangeStart', function(event, next, current) {
            checkUserSession(next, current);
        });

        $rootScope.Logout = function() {
            AuthService.ClearCredentials();
            $location.path('/core/login/');
        }

    }])
    .config(['uiSelectConfig', function(uiSelectConfig) {
        uiSelectConfig.theme = 'bootstrap';
    }])
    .config(function($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    })
    .config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

        $urlRouterProvider.otherwise('/app/dashboard');

        $stateProvider

        //app core pages (errors, login,signup)
            .state('core', {
                abstract: true,
                url: '/core',
                template: '<div ui-view></div>',
                authenticated: false
            })
            .state('core.login', {
                url: '/login/?origin',
                controller: 'LoginCtrl',
                templateUrl: 'views/tmpl/login.html'
            })
            .state('core.forgotpass', {
                url: '/forgotpass',
                controller: 'ForgotPasswordCtrl',
                templateUrl: 'views/tmpl/forgotpass.html'
            })
            .state('core.forgotpass-success', {
                url: '/forgotpass/success',
                controller: 'ForgotPasswordSuccessCtrl',
                templateUrl: 'views/tmpl/forgotpass-success.html'
            })


        .state('app', {
            abstract: true,
            url: '/app',
            templateUrl: 'views/tmpl/app.html',
            authenticated: true
        })

        //dashboard
        .state('app.dashboard', {
            url: '/dashboard',
            controller: 'DashboardCtrl',
            templateUrl: 'views/tmpl/dashboard.html',
        })

        //explorer
        .state('app.purchase', {
            url: '/purchase',
            controller: 'PurchaseCtrl',
            templateUrl: 'views/tmpl/purchase.html',
            containerClass: 'sidebar-xs-forced sidebar-xs'
        })

        //explorer
        .state('app.corporation', {
            url: '/corporation',
            controller: 'CorporationCtrl',
            templateUrl: 'views/tmpl/corporation.html',
            containerClass: 'sidebar-xs-forced sidebar-xs'
        })

        //explorer
        .state('app.collections', {
                url: '/collections',
                controller: 'CollectionsCtrl',
                templateUrl: 'views/tmpl/collections.html',
                containerClass: 'sidebar-xs-forced sidebar-xs'
            })
            //explorer
            .state('app.collections.navigator', {
                url: '/collections/navigator',
                controller: 'NavigatorCtrl',
                templateUrl: 'views/tmpl/collections.html',
                containerClass: 'sidebar-xs-forced sidebar-xs'
            });
    }]);
