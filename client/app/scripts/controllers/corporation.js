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
            title: $rootScope.globals.currentUser.corporation.name
        };

        $scope.corporation = Corporation.get({id:$rootScope.globals.currentUser.corporation.id});

        $scope.onSubmit = function() {
        	var data = {name:  $scope.corporation.name, document: $scope.corporation.document }
        	Corporation
        		.update({id:$rootScope.globals.currentUser.corporation.id}, data)
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