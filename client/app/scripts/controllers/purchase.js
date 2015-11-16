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

        $scope.filter = {
            person: {
                nature: ''
            }
        };


        $scope.counting = true;
        $scope.natures = [{
            id: 'P',
            name: 'Pessoa Física'
        }, {
            id: 'L',
            name: 'Pessoa Jurídica'
        }];

        $scope.carriers = Carrier.query();
        $scope.areacodes = Areacode.query();
        $scope.cities = City.query();


        $scope.count = 0;

        $scope.updateCount = function() {

            $scope.counting = true;

            var data = {}

            try {
                if ($scope.filter.person.nature && $scope.filter.person.nature.length && $scope.filter.person.nature.length < $scope.natures.length) {
                    data.nature = $scope.filter.person.nature.join('|');
                }
            } catch (error) {}

            try {
                if ($scope.filter.contact.phone.carrier && $scope.filter.contact.phone.carrier.length && $scope.filter.contact.phone.carrier.length < $scope.carriers.length) {

                    data.carrier = $scope.filter.contact.phone.carrier.join('|');
                }
            } catch (error) {}

            try {
                if ($scope.filter.contact.phone.areacode && $scope.filter.contact.phone.areacode.length && $scope.filter.contact.phone.areacode.length < $scope.areacodes.length) {

                    data.areacode = $scope.filter.contact.phone.areacode.join('|');
                }
            } catch (error) {}

            try {
                if ($scope.filter.contact.phone.address.city && $scope.filter.contact.phone.address.city.length && $scope.filter.contact.phone.address.city.length < $scope.cities.length) {

                    data.city = $scope.filter.contact.phone.address.city.join('|');
                }
            } catch (error) {}

            var params = jQuery.param(data);

            $http
                .get('http://10.46.80.80:8080/person/count/?' + params)
                .then(
                    function(response) {
                        $scope.count = response.data;
                        $scope.counting = false;
                    },
                    function(response) {

                    }
                );
        }

        $scope.$watch('filter', $scope.updateCount, true);

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
