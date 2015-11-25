'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:ExplorerCtrl
 * @description
 * # ExplorerCtrl
 * Controller of the CONTACTPRO
 */
app
    .controller('PurchaseCtrl', 
        ['$scope', '$http', 'Cart', 'Criteria', 'Carrier', 'Areacode', 'City', 'Neighborhood', 
        function($scope, $http, Cart, Criteria, Carrier, Areacode, City, Neighborhood) {
            $scope.page = {
                title: 'Comprar coleção de registros',
                subtitle: 'Place subtitle here...'
            };

            $scope.counting = true;
            $scope.updating = true;

            $scope.filter = {
                nature: '',
                carrier: '',
                areacode: '',
                city: '',
                neighborhood: ''
            };

            $scope.cart = Cart.query();

            $scope.natures = [{
                id: 'P',
                name: 'Pessoa Física'
            }, {
                id: 'L',
                name: 'Pessoa Jurídica'
            }];

            $scope.carriers = [];
            $scope.areacodes = [];
            $scope.cities = [];
            $scope.neighborhoods = [];

            $scope.count = 0;

            $scope.addCriteria = function() {
                $scope.cart = Criteria.save({}, $scope.filter)
            }

            $scope.deleteCriteria = function() {
                $scope.cart = Criteria.delete({}, $scope.filter)
            }

            $scope.updateCarriers = function() {

                if ($scope.filter.nature) {

                    $scope.updating = true;

                    $scope.carriers = Carrier.query({
                        nature: $scope.filter.nature
                    });

                    $scope.carriers.$promise.then(function(result) {
                        $scope.carriers = result;

                        $scope.areacodes = [];
                        $scope.cities = [];
                        $scope.neighborhoods = [];

                        $scope.updateCount();
                    });

                }
            }

            $scope.updateAreacodes = function() {

                if ($scope.filter.carrier) {

                    $scope.updating = true;

                    $scope.areacodes = Areacode.query({
                        nature: $scope.filter.nature,
                        carrier: $scope.filter.carrier
                    });

                    $scope.areacodes.$promise.then(function(result) {
                        $scope.areacodes = result;

                        $scope.cities = [];
                        $scope.neighborhoods = [];
                        $scope.updateCount();
                    });

                }
            }

            $scope.updateCities = function() {

                if ($scope.filter.areacode) {

                    $scope.updating = true;

                    $scope.cities = City.query({
                        nature: $scope.filter.nature,
                        carrier: $scope.filter.carrier,
                        areacode: $scope.filter.areacode
                    });

                    $scope.cities.$promise.then(function(result) {
                        $scope.cities = result;

                        $scope.neighborhoods = [];

                        $scope.updateCount();
                    });

                }

            }

            $scope.updateNeighborhoods = function() {

                if ($scope.filter.city) {

                    $scope.updating = true;

                    $scope.neighborhoods = Neighborhood.query({
                        nature: $scope.filter.nature,
                        carrier: $scope.filter.carrier,
                        areacode: $scope.filter.areacode,
                        city: $scope.filter.city
                    });

                    $scope.neighborhoods.$promise.then(function(result) {
                        $scope.neighborhoods = result;
                        $scope.updateCount();
                    });
                }
            }

            $scope.updateCount = function() {

                $scope.counting = true;
                $scope.updating = true;

                var params = jQuery.param($scope.filter);

                $http
                    .get('http://10.46.80.80:8080/filter/person/count/?' + params)
                    .then(
                        function(response) {
                            $scope.count = response.data.count;
                        },
                        function(response) {
                            console.log(response);
                        }
                    )
                    .finally(
                        function() {
                            $scope.counting = false;
                            $scope.updating = false;
                        }
                    );
            }

            $scope.$watch('filter.nature', $scope.updateCarriers, true);
            $scope.$watch('filter.carrier', $scope.updateAreacodes);
            $scope.$watch('filter.areacode', $scope.updateCities);
            $scope.$watch('filter.city', $scope.updateNeighborhoods, true);
            $scope.$watch('filter.neighborhood', $scope.updateCount, true);

        }
    ])
    .filter('cpf', function() {
        return function(item) {
            return item.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/g, "\$1.\$2.\$3\-\$4");
        }
    })
    .filter('cnpj', function() {
        return function(item) {
            return item.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/g, "\$1.\$2.\$3\/\$4\-\$5");
        }
    })
    .filter("brl", function(numberFilter) {
        function isNumeric(value) {
            return (!isNaN(parseFloat(value)) && isFinite(value));
        }

        return function(inputNumber) {
            if (isNumeric(inputNumber)) {
                // Default values for the optional arguments
                var currencySymbol = "";
                var decimalSeparator = ",";
                var thousandsSeparator = ".";
                var decimalDigits = 2;

                if (decimalDigits < 0) decimalDigits = 0;

                // Format the input number through the number filter
                // The resulting number will have "," as a thousands separator
                // and "." as a decimal separator.
                var formattedNumber = numberFilter(inputNumber, decimalDigits);

                // Extract the integral and the decimal parts
                var numberParts = formattedNumber.split(".");

                // Replace the "," symbol in the integral part
                // with the specified thousands separator.
                numberParts[0] = numberParts[0].split(",").join(thousandsSeparator);

                // Compose the final result
                var result = currencySymbol + numberParts[0];

                if (numberParts.length == 2) {
                    result += decimalSeparator + numberParts[1];
                }

                return result;
            } else {
                return inputNumber;
            }
        };
    });
