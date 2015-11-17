'use strict';

app
    .factory('Carrier', function($resource){
        return $resource(
            'http://10.46.80.80:8080/filter/carrier/'
        );
    })
    .factory('Areacode', function($resource){
        return $resource(
            'http://10.46.80.80:8080/filter/areacode/'
        );
    })
    .factory('City', function($resource){
        return $resource(
            'http://10.46.80.80:8080/filter/city/'
        );
    })
    .factory('Neighborhood', function($resource){
        return $resource(
            'http://10.46.80.80:8080/filter/neighborhood/'
        );
    });

