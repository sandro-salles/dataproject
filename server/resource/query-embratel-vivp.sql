select
	distinct on (person.id)
	person.id,
	person.name,
	person.document,
	person.nature,
	phone.phone_id,
	phone.phone_areacode,
	phone.phone_number,
	phone.carrier_name,
	address.id as address_id,
	address.state as address_state,
	address.city as address_city,
	address.neighborhood as address_neighborhood,
	address.location as address_location,
	address.zipcode as address_zipcode
from 
	person_person as person
	inner join lateral
		(
			select
				carrier.name as carrier_name,
				_phone.id as phone_id,
				_phone.areacode as phone_areacode,
				_phone.number as phone_number,
				_phone.address_id,
				p_phone.person_id as person_id
			from
				contact_phone as _phone
			inner join
				contact_personphone as p_phone
					on (p_phone.phone_id = _phone.id and p_phone.person_id = person.id)
			inner join
				contact_carrier as carrier
					on (carrier.id = _phone.carrier_id)
			where
				_phone.areacode = 11
				and _phone.carrier_id in (2,3)
			limit 1
		) as phone
		on true
	inner join lateral
		(
			select
				id,
				state,
				city,
				neighborhood,
				location,
				zipcode
			from
				contact_address
			where
				id = 	phone.address_id
			limit 1	
		) as address
		on true
where
	person.nature = 'P'
	and 
	(
		(
			address.city = 'SAO PAULO'
			and
			address.neighborhood in ('SANTANA', 'CERQUEIRA CESAR', 'JARDIM PAULISTANO', 'JARDIM AMERICA', 'JARDIM PAUISTA', 'JARDIM EUROPA', 'BARRA FUNDA', 'PERDIZES')
		)
		OR
		
		address.city = 'GUARULHOS'
	)		
order by
	person.id asc	
limit 40000;