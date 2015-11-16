CREATE MATERIALIZED VIEW
contact_address_city as select distinct city from contact_address order by city asc;

CREATE MATERIALIZED VIEW
contact_address_city_neighborhood as select distinct on (city, neighborhood)  city || '_' || neighborhood as id, city, neighborhood from contact_address order by city asc, neighborhood asc;

CREATE MATERIALIZED VIEW
contact_phone_areacode as select distinct areacode from contact_phone order by areacode asc;