'use strict';

app
    .factory('AuthService', AuthService);

AuthService.$inject = ['$http', '$cookieStore', '$rootScope', '$timeout', 'jwtHelper'];

function AuthService($http, $cookieStore, $rootScope, $timeout, jwtHelper) {
    var service = {};

    service.Login = Login;
    service.SetCredentials = SetCredentials;
    service.ClearCredentials = ClearCredentials;

    return service;

    function Login(username, password, success_callback, error_callback) {

        /* Dummy authentication for testing, uses $timeout to simulate api call
         ----------------------------------------------*/
        $timeout(function() {
            var response;
            var data = {
                'username': username,
                'password': password
            };

            $http
                .post('http://10.46.80.80:8080/api-token-auth/', data)
                .then(
                    function(response) {
                        success_callback(response);
                    },
                    function(response) {
                        error_callback(response)
                    }
                );

        }, 1000);

        /* Use this for real authentication
         ----------------------------------------------*/
        //$http.post('/api/authenticate', { username: username, password: password })
        //    .success(function (response) {
        //        callback(response);
        //    });

    }

    function RefreshToken(token) {

    }

    function SetCredentials(authdata) {

        var currentUser = authdata.user;
        currentUser.token = authdata.token;

        $rootScope.globals = {
            currentUser: currentUser
        };

        $http.defaults.headers.common['Authorization'] = 'JWT ' + authdata.token; // jshint ignore:line
        $cookieStore.put('globals', $rootScope.globals);
    }

    function ClearCredentials() {
        $rootScope.globals = {};
        $cookieStore.remove('globals');
        $http.defaults.headers.common.Authorization = 'JWT';
    }
}
