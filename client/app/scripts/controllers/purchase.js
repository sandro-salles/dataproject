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
        ['$scope', '$http', 'Cart', 'Criteria', 'State', 'Carrier', 'Areacode', 'City', 'Neighborhood', 
        function($scope, $http, Cart, Criteria, State, Carrier, Areacode, City, Neighborhood) {
            $scope.page = {
                title: 'Comprar coleção de registros',
                subtitle: 'Place subtitle here...'
            };

            $scope.counting = true;
            $scope.updating = true;

            $scope.filter = {
                nature: '',
                state: '',
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

            $scope.states = [];
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

            $scope.updateStates = function() {

                $scope.updating = true;

                $scope.filter.state, $scope.filter.carrier, $scope.filter.areacode, $scope.filter.city, $scope.filter.neighborhood = '';  
                    
                $scope.states = [];
                $scope.carriers = [];
                $scope.areacodes = [];
                $scope.cities = [];
                $scope.neighborhoods = [];

                if ($scope.filter.nature) {

                    $scope.states = State.query({
                        nature: $scope.filter.nature
                    });

                    $scope.states.$promise.then(function(result) {
                        $scope.states = result;

                        $scope.updateCount();
                    });

                } else {
                    $scope.updateCount();
                }
            }

            $scope.updateCarriers = function() {

                $scope.updating = true;

                $scope.filter.carrier, $scope.filter.areacode, $scope.filter.city, $scope.filter.neighborhood = '';  
                
                $scope.carriers = [];
                $scope.areacodes = [];
                $scope.cities = [];
                $scope.neighborhoods = [];

                if ($scope.filter.state) {

                    $scope.carriers = Carrier.query({
                        nature: $scope.filter.nature,
                        state: $scope.filter.state
                    });

                    $scope.carriers.$promise.then(function(result) {
                        $scope.carriers = result;
                        $scope.updateCount();
                    });

                } else {
                    $scope.updateCount();
                }
            }

            $scope.updateAreacodes = function() {

                if ($scope.filter.carrier) {

                    $scope.updating = true;

                    $scope.filter.areacode, $scope.filter.city, $scope.filter.neighborhood = '';  
                    
                    $scope.areacodes = [];
                    $scope.cities = [];
                    $scope.neighborhoods = [];

                    $scope.areacodes = Areacode.query({
                        nature: $scope.filter.nature,
                        state: $scope.filter.state,
                        carrier: $scope.filter.carrier
                    });

                    $scope.areacodes.$promise.then(function(result) {
                        $scope.areacodes = result;

                        $scope.updateCount();
                    });

                }
            }

            $scope.updateCities = function() {

                if ($scope.filter.areacode) {

                    $scope.updating = true;

                    $scope.filter.city, $scope.filter.neighborhood = '';  
                    
                    $scope.cities = [];
                    $scope.neighborhoods = [];

                    $scope.cities = City.query({
                        nature: $scope.filter.nature,
                        state: $scope.filter.state,
                        carrier: $scope.filter.carrier,
                        areacode: $scope.filter.areacode
                    });

                    $scope.cities.$promise.then(function(result) {
                        $scope.cities = result;
                        $scope.updateCount();
                    });

                }

            }

            $scope.updateNeighborhoods = function() {

                if ($scope.filter.city) {

                    $scope.updating = true;

                    $scope.filter.neighborhood = '';  
                    
                    $scope.neighborhoods = [];


                    $scope.neighborhoods = Neighborhood.query({
                        nature: $scope.filter.nature,
                        state: $scope.filter.state,
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

            $scope.$watch('filter.nature', $scope.updateStates, true);
            $scope.$watch('filter.state', $scope.updateCarriers);
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
