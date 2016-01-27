from django.core.cache import cache
from django.db import connection
from django.conf import settings
import mmh3


class PersonCounter:

    PARAM_KEYS = ['nature', 'state', 'carrier', 'areacode', 'city', 'neighborhood']

    COUNT_BASE_QUERY = """
        SELECT 
            COUNT(DISTINCT person.id)
        FROM
            person_person as person
            INNER JOIN
                contact_personphone cpp
                ON (cpp.person_id = person.id)
            INNER JOIN
                contact_phone as cp
                ON (cp.id = cpp.phone_id)
            INNER JOIN
                contact_address as ca
                ON (ca.id = cp.address_id)
        where
        """

    @staticmethod
    def build_key(params):

        joined = ','.join(['%s=%s' % (PersonCounter.PARAM_KEYS[i], value) for i, value in enumerate(params) if value])
        return 'person-count__%s' % mmh3.hash128(joined)

    @staticmethod
    def build_query(params):
            
        nature, state, carrier, areacode, city, neighborhood = params

        query = " 0 = 0 "

        if nature:
            query += " and person.nature = '%s'" % nature
        
        if state:
            query += " and ca.state = '%s'" % state

        if carrier:
            query += " and cp.carrier_id = %s" % carrier

        if areacode:
            query += " and cp.areacode = %s" % areacode

        if city:
            query += " and ca.city = '%s'" % city

        if neighborhood:
            query += " and ca.neighborhood = '%s'" % neighborhood

        return '(%s)' % query

    @staticmethod
    def count(params):


        if params:
            if len(params) > 1:
                
                #import pdb; pdb.set_trace()

                queries = []

                for param in params:

                    queries.append(PersonCounter.build_query(param))
                
                query = ' OR '.join(queries)
                
                query = '%s %s' % (PersonCounter.COUNT_BASE_QUERY, query)

                cursor = connection.cursor()

                cursor.execute(query)

                count = cursor.fetchone()[0]

            else:

                cache_key = PersonCounter.build_key(params[0])
                count = cache.get(cache_key, settings.CACHE_EXPIRED_IDENTIFIER)

                if str(count) == settings.CACHE_EXPIRED_IDENTIFIER:

                    cursor = connection.cursor()
                    
                    query = PersonCounter.build_query(params[0])
                    query = '%s %s' % (PersonCounter.COUNT_BASE_QUERY, query)

                    cursor.execute(query)

                    count = cursor.fetchone()[0]

                    cache.set(cache_key, count)

            return count
        
        return 0
