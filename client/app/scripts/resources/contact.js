'use strict';

app
    .factory('Carrier', function($resource){
        return $resource(
            'http://10.46.80.80:8080/contact/phone/carrier/:id/', 
            { id: '@id'}
        );
    })
    .factory('Areacode', function($resource){
        return $resource(
            'http://10.46.80.80:8080/contact/phone/areacode/:id/', 
            { id: '@id'}
        );
    })
    .factory('City', function($resource){
        return $resource(
            'http://10.46.80.80:8080/contact/address/city/:id/', 
            { id: '@id'}
        );
    })
    .factory('Neighborhood', function($resource){
        return $resource(
            'http://10.46.80.80:8080/contact/address/city/neighborhood/:id/', 
            { id: '@id'}
        );
    });

