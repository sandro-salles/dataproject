from django.core.cache import cache
from django.db import connection
from django.conf import settings
import mmh3


class PersonCounter:

    PARAM_KEYS = ['nature', 'carrier', 'areacode', 'city', 'neighborhood']

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
            0 = 0
        """

    @staticmethod
    def build_key(params):
        joined = ','.join(['%s=%s' % (PersonCounter.PARAM_KEYS[i], value) for i, value in enumerate(params) if value is not None])
        return 'person-count__%s' % mmh3.hash128(joined)


    @staticmethod
    def count(params):

        cache_key = PersonCounter.build_key(params)
        count = cache.get(cache_key, settings.CACHE_EXPIRED_IDENTIFIER)

        if str(count) == settings.CACHE_EXPIRED_IDENTIFIER:

            nature, carrier, areacode, city, neighborhood = params

            query = PersonCounter.COUNT_BASE_QUERY

            if nature:
                query += " and person.nature = '%s'" % nature

            if carrier:
                query += " and cp.carrier_id = %s" % carrier

            if areacode:
                query += " and cp.areacode = %s" % areacode

            if city:
                query += " and ca.city = '%s'" % city

            if neighborhood:
                query += " and ca.neighborhood = '%s'" % neighborhood


            cursor = connection.cursor()

            cursor.execute(query)

            count = cursor.fetchone()[0]

            cache.set(cache_key, count)

        return count