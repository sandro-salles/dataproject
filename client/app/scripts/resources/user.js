'use strict';

app
    .factory('User', function($resource){
        return $resource(
            'http://10.46.80.80:8080/user/:id', 
            { id: '@id'}
        );
    });

