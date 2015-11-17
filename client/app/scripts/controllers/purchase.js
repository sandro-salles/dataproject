'use strict';

/**
 * @ngdoc function
 * @name CONTACTPRO.controller:ExplorerCtrl
 * @description
 * # ExplorerCtrl
 * Controller of the CONTACTPRO
 */
app
    .controller('PurchaseCtrl', ['$scope', '$http', 'Carrier', 'Areacode', 'City', 'Neighborhood', function($scope, $http, Carrier, Areacode, City, Neighborhood) {
        $scope.page = {
            title: 'Comprar coleção de registros',
            subtitle: 'Place subtitle here...'
        };

        $scope.counting = true;

        $scope.filter = {
            person: {
                nature: ''
            },
            contact: {
                phone: {
                    carrier: ''
                }
            }
        };
        
        $scope.cart = {}
        
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

        $scope.updateCarriers = function() {
            

            try {
                if ($scope.filter.nature) {
                    $scope.carriers = Carrier.query({nature:$scope.filter.nature});
                    $scope.updateCount();      
                }                
            } catch(error) {}            
        }

        $scope.updateAreacodes = function() {
            try {
                if ($scope.filter.carrier) {
                    $scope.areacodes = Areacode.query({carrier:$scope.filter.carrier});
                    $scope.updateCount();
                }
            } catch(error) {}
        }

        $scope.updateCities = function() {
            try {
                if ($scope.filter.areacode) {
                    $scope.cities = City.query({areacode:$scope.filter.areacode});
                    $scope.updateCount();
                }
            } catch(error) {}
        }

        $scope.updateNeighborhoods = function() {
            try {
                if ($scope.filter.city) {
                    $scope.neighborhoods = Neighborhood.query({city:$scope.filter.city});
                    $scope.updateCount();
                }
            } catch(error) {}
        }

        $scope.updateCount = function() {

            $scope.counting = true;

            var data = {}

            try {
                if ($scope.filter.nature) {
                    data.nature = $scope.filter.nature;
                }
            } catch (error) {}

            try {
                if ($scope.filter.carrier) {
                    data.carrier = $scope.filter.carrier;
                }
            } catch (error) {}

            try {
                if ($scope.filter.areacode) {
                    data.areacode = $scope.filter.areacode;
                }
            } catch (error) {}

            try {
                if ($scope.filter.city) {
                    data.city = $scope.filter.city;
                }
            } catch (error) {}
            
            try {
                if ($scope.filter.neighborhood) {
                    data.neighborhood = $scope.filter.neighborhood;
                }
            } catch (error) {}

            var params = jQuery.param(data);

            $http
                .get('http://10.46.80.80:8080/filter/person/count/?' + params)
                .then(
                    function(response) {
                        $scope.count = response.data.count;
                        $scope.counting = false;
                    },
                    function(response) {
                        console.log(response);
                    }
                );
        }

        $scope.$watch('filter.nature', $scope.updateCarriers, true);
        $scope.$watch('filter.carrier', $scope.updateAreacodes);
        $scope.$watch('filter.areacode', $scope.updateCities);
        $scope.$watch('filter.city', $scope.updateNeighborhoods, true);
        $scope.$watch('filter.neighborhood', $scope.updateCount, true);

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
