'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:AccountCtrl
 * @description
 * # AccountCtrl
 * Controller of the CONTACTPRO
 */
app
    .controller('CorporationCtrl', ['$rootScope', '$scope', 'toastr', 'Corporation', function($rootScope, $scope, toastr, Corporation) {
        $scope.page = {
            title: $rootScope.globals.currentUser.account.corporation.name
        };

        $scope.corporation = Corporation.get({id:$rootScope.globals.currentUser.account.corporation.id});

        $scope.onSubmit = function() {
        	var data = {name:  $scope.corporation.name, document: $scope.corporation.document }
        	Corporation
        		.update({id:$rootScope.globals.currentUser.account.corporation.id}, data)
        		.$promise.then(
        			function(data) {
        				toastr.success('Sucesso!');
        			}, 
        			function(error) {
        				if(error.status == 401) {
        					//
        				}
        			}
    			);
        };

    }]);