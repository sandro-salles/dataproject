'use strict';

/**
 * @ngdoc function
 * @name DATAPROJECT.controller:ExplorerCtrl
 * @description
 * # ExplorerCtrl
 * Controller of the DATAPROJECT
 */
app
    .controller('ExplorerCtrl', ['$scope', '$http', 'Person', function($scope, $http, Person) {
        $scope.page = {
            title: 'Data Explorer',
            subtitle: 'Place subtitle here...'
        };

        $scope.paginate_by = 100;

        $scope.count = 0;        
        $scope.next = null;
        $scope.previous = null;

        $scope.update_count = function(data, headers) {
            $scope.count = headers('count');        
            $scope.next = headers('next');
            $scope.previous = headers('previous');
        };

        $scope.people = Person.query({
            nature: 'L',
            phones__carrier__slug: 'gvt-fixo'
        }, $scope.update_count);

        $scope.selectedAll = false;

        

        $scope.selectAll = function() {
            angular.forEach($scope.people, function(person) {
                person.selected = $scope.selectedAll;
            });
        };
    }])
    .filter('cpf', function() {
        return function(item) {
            return item.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/g, "\$1.\$2.\$3\-\$4");
        }
    })
    .filter('cnpj', function() {
        return function(item) {
            return item.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/g, "\$1.\$2.\$3\/\$4\-\$5");
        }
    });
