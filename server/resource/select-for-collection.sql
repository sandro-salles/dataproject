select
	distinct on (person.id)
	person.id,
	row_to_json((
		SELECT _json FROM (
			SELECT 
				row_to_json((SELECT p_json FROM (SELECT person.name, person.document, person.updated_at) p_json)) as "person"			) _json
	))	
from 
	person_person as person
where
	person.nature = 'P'
	and EXISTS (SELECT 1 FROM contact_phone cp inner join contact_personphone as cpp on (cpp.phone_id = cp.id) where cpp.person_id = person.id and cp.areacode = 11)
limit 1;