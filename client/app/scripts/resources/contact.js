'use strict';

app
    .factory('Carrier', function($resource){
        return $resource(
            'http://10.46.80.80:8080/contact/phone/carrier/'
        );
    })
    .factory('Areacode', function($resource){
        return $resource(
            'http://10.46.80.80:8080/contact/phone/areacode/'
        );
    })
    .factory('City', function($resource){
        return $resource(
            'http://10.46.80.80:8080/contact/address/city/'
        );
    })
    .factory('Neighborhood', function($resource){
        return $resource(
            'http://10.46.80.80:8080/contact/address/neighborhood/'
        );
    });

