CREATE MATERIALIZED VIEW
contact_address_city as select distinct city from contact_address order by city asc;


CREATE MATERIALIZED VIEW
contact_phone_areacode as select distinct areacode from contact_phone order by areacode asc;


CREATE MATERIALIZED VIEW
person_nature_contact_phone_carrier as 
select 
	distinct on (person.nature, cp.carrier_id)  
	person.nature || '_' || cp.carrier_id as id, 
	person.nature, 
	cp.carrier_id 
from person_person as person
	inner join
		contact_personphone as cpp
		on (cpp.person_id = person.id)
	inner join
		contact_phone as cp
		on (cp.id = cpp.phone_id)
	order by person.nature asc, cp.carrier_id asc;



CREATE MATERIALIZED VIEW
contact_phone_carrier_contact_phone_areacode as 
select 
	distinct on (cp.carrier_id, cp.areacode) 
	cp.carrier_id || '_' || cp.areacode as id, 
	cp.carrier_id, 
	cp.areacode 
from contact_phone as cp
order by cp.carrier_id asc, cp.areacode asc;




CREATE MATERIALIZED VIEW
contact_phone_areacode_contact_address_city as 
select 
	distinct on (cp.areacode, ca.city) 
	cp.areacode || '_' || ca.city as id, 
	cp.areacode, 
	ca.city 
from contact_phone as cp
	inner join
		contact_address as ca
			on (ca.id = cp.address_id)

order by cp.areacode asc, ca.city asc;


CREATE MATERIALIZED VIEW
contact_address_city_contact_address_neighborhood as select distinct on (city, neighborhood)  city || '_' || neighborhood as id, city, neighborhood from contact_address order by city asc, neighborhood asc;





CREATE MATERIALIZED VIEW
materialized_filter as 
select 
	distinct on (person.nature, cp.carrier_id, cp.areacode, ca.city, ca.neighborhood)
	row_number() 
		over (		
			order by 
				person.nature asc,
				cp.carrier_id asc, 
				cp.areacode asc, 
				ca.city asc, 
				ca.neighborhood asc
		) id,
	person.nature, 
	cp.carrier_id, 
	cp.areacode, 
	ca.city, 
	ca.neighborhood
from person_person as person
	inner join
		contact_personphone as cpp
		on (cpp.person_id = person.id)
	inner join
		contact_phone as cp
		on (cp.id = cpp.phone_id)
	inner join
		contact_address as ca
			on (ca.id = cp.address_id)
order by 
	person.nature asc, 
	cp.carrier_id asc, 
	cp.areacode asc, 
	ca.city asc, 
	ca.neighborhood asc;




create index on materialized_filter (nature);
create index on materialized_filter (areacode);
create index on materialized_filter (city);
create index on materialized_filter (neighborhood);









