'use strict';

app
    .factory('AuthService', AuthService);

AuthService.$inject = ['$injector', '$cookieStore', '$rootScope', '$timeout', 'jwtHelper'];

function AuthService($injector, $cookieStore, $rootScope, $timeout, jwtHelper) {
    var service = {};


    service.Login = Login;
    service.SetCredentials = SetCredentials;
    service.ClearCredentials = ClearCredentials;
    service.RefreshToken = RefreshToken;

    return service;

    function Login(username, password, success_callback, error_callback) {

        var data = {
            'username': username,
            'password': password
        };

        $injector.get("$http")
            .post('http://10.46.80.80:8080/api-token-auth/', data)
            .then(
                function(response) {
                    success_callback(response);
                },
                function(response) {
                    error_callback(response)
                }
            );
    }

    function RefreshToken(token, success_callback, error_callback) {

        $injector.get("$http")
            .post('http://10.46.80.80:8080/api-token-refresh/', {
                token: token
            })
            .then(
                function(response) {
                    service.SetCredentials(response.data);
                    success_callback(response);
                },
                function(response) {
                    service.ClearCredentials();
                    error_callback(response)
                }
            );
    }

    function SetCredentials(authdata) {

        var currentUser = authdata.user;
        currentUser.token = authdata.token;

        $rootScope.globals = {
            currentUser: currentUser
        };

        $injector.get("$http").defaults.headers.common['Authorization'] = 'JWT ' + authdata.token; // jshint ignore:line
        $cookieStore.put('globals', $rootScope.globals);
    }

    function ClearCredentials() {
        $rootScope.globals = {};
        $cookieStore.remove('globals');
        $injector.get("$http").defaults.headers.common.Authorization = 'JWT';
    }
}

app
    .factory('RefreshAuthTokenInterceptor', RefreshAuthTokenInterceptor)
    .config(['$httpProvider', function($httpProvider) {
        $httpProvider.interceptors.push('RefreshAuthTokenInterceptor');
    }]);

RefreshAuthTokenInterceptor.$inject = ['$rootScope', '$q', 'jwtHelper', 'AuthService'];

function RefreshAuthTokenInterceptor($rootScope, $q, jwtHelper, AuthService) {

    var requestInterceptor = {

        request: function(config) {


            var deferred = $q.defer();

            var is_auth_request = (config.url.indexOf('/api-token') > -1);


            if (!is_auth_request && $rootScope.globals.currentUser && $rootScope.globals.currentUser.token) {

                var exp = moment(jwtHelper.getTokenExpirationDate($rootScope.globals.currentUser.token));
                var now = moment(new Date());

                if (exp.diff(now, 'minutes') <= 2) {

                    console.log('token about to expire... refreshing');
                    
                    AuthService.RefreshToken(
                        $rootScope.globals.currentUser.token,
                        function(response) {
                            deferred.resolve(config);
                        },
                        function(response) {
                            deferred.resolve(config);
                        }
                    );
                } else {
                    deferred.resolve(config);
                }


            } else {
                deferred.resolve(config);
            }


            return deferred.promise;
        }
    };

    return requestInterceptor;
}
