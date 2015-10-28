'use strict';

app
    .factory('Person', function($resource){
        return $resource(
            'http://10.46.80.80:8080/person/:id', 
            { id: '@id'}, 
            {
                query : {
                    method: 'GET', 
                    isArray: true, 
                    transformResponse : function(data, headers) {
                        data = JSON.parse(data);
                        headers()['count'] = data.count;
                        headers()['next'] = data.next;
                        headers()['previous'] = data.previous;
                        return data.results;
                    }
                }
            }
        );
    });

