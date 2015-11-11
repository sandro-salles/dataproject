'use strict';

app
    .factory('Corporation', function($resource){
        return $resource(
            'http://10.46.80.80:8080/account/corporation/:id/', 
            { id: '@id'},
            {
		        'update': { method:'PUT' }
		    }
        );
    });

