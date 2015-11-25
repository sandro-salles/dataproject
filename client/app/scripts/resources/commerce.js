'use strict';

app
    .factory('Cart', function($resource){
        return $resource(
            'http://10.46.80.80:8080/commerce/cart/:id/',
            { id: '@id'},
            {'query': {method: 'GET', isArray: false }}
        );
    })
    .factory('Criteria', function($resource){
        return $resource(
            'http://10.46.80.80:8080/commerce/cart/checkout/criteria/:id/',
            { id: '@id'}
        );
    });

