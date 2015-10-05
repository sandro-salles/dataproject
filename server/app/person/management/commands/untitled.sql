CREATE OR REPLACE FUNCTION prepare_for_import(
	document__hash integer,    
	phone__hash integer,
	address__hash integer,
	phone__carrier_id integer,
	address__zipcode varchar,
	person__name varchar
)

RETURNS TABLE ( 
  		person_id integer, 
  		person_is_dirty boolean, 
  		document_id integer, 
  		phone_id integer, 
  		phone_carrier_has_changed boolean, 
  		phone_relation_is_new boolean, 
  		address_id integer, 
  		street_id integer, 
  		neighborhood_id integer, 
  		city_id integer,
  		state_id varchar,
  		address_relation_is_new boolean 
) AS
$BODY$
BEGIN
	RETURN QUERY WITH 
	  cte_phone as  (
	    SELECT 
	      phone.contact_ptr_id as phone_id, 
	      phone.carrier_id as carrier_id
	    FROM 
	      contact_phone phone
	    WHERE 
	      phone.hash = phone__hash 
	    LIMIT 1
	  ),
	  cte_address as (
	    SELECT 
	      address.contact_ptr_id as address_id,
	      street.log_nu_sequencial as street_id,
	      0 as neighborhood_id,
	      0 as city_id,
	      cast(text '' as varchar) as state_id
	    FROM 
	      contact_address address
	    INNER JOIN
	      log_logradouro street
	        ON (street.log_nu_sequencial = address.street_id)
	    WHERE 
	      address.hash = address__hash
	    UNION ALL
	      SELECT 
	        NULL,
	        street.log_nu_sequencial as street_id,
		    0 as neighborhood_id,
		    0 as city_id,
		    cast(text '' as varchar) as state_id
	      FROM 
	        log_logradouro street
	      WHERE 
	        NOT EXISTS (SELECT 1 FROM contact_address address WHERE address.hash = address__hash) 
	        AND street.cep = address__zipcode
	      LIMIT 1
	  )
	SELECT 
	  person.id as person_id,
	  (CASE WHEN person.id IS NOT NULL AND person.name <> person__name THEN true ELSE false END) as person_is_dirty,
	  doc.id as document_id,   
	  (SELECT cte_phone.phone_id FROM cte_phone LIMIT 1) as phone_id,
	  (SELECT (CASE WHEN cte_phone.carrier_id IS NOT NULL AND cte_phone.carrier_id <> phone__carrier_id THEN true ELSE false END) FROM cte_phone LIMIT 1) as phone_carrier_has_changed,
	  (CASE WHEN cphonep.id IS NULL THEN true ELSE false END) as phone_relation_is_new,
	  (SELECT cte_address.address_id FROM cte_address LIMIT 1) as address_id,  
	  (SELECT cte_address.street_id FROM cte_address LIMIT 1) as street_id,   
	  (SELECT cte_address.neighborhood_id FROM cte_address LIMIT 1) as neighborhood_id,  
	  (SELECT cte_address.city_id FROM cte_address LIMIT 1) as city_id,  
	  (SELECT cte_address.state_id FROM cte_address LIMIT 1) as state_id,  
	  (CASE WHEN caddressp.id IS NULL THEN true ELSE false END) as address_relation_is_new
	FROM 
	  document_document doc 
	INNER JOIN 
	  person_person person 
	    ON (person.id = doc.person_id)
	LEFT OUTER JOIN
	  contact_contact_persons cphonep
	    ON (
	      cphonep.person_id = person.id 
	      AND cphonep.contact_id IN (SELECT cte_phone.phone_id FROM cte_phone LIMIT 1)
	      AND (SELECT cte_phone.phone_id FROM cte_phone LIMIT 1) IS NOT NULL
	    )
	LEFT OUTER JOIN
	  contact_contact_persons caddressp
	    ON (
	      caddressp.person_id = person.id 
	      AND caddressp.contact_id IN (SELECT cte_address.address_id FROM cte_address LIMIT 1)
	      AND (SELECT cte_address.address_id FROM cte_address LIMIT 1) IS NOT NULL   )
	WHERE 
	  doc.hash = document__hash
	UNION ALL
	  SELECT 
	    NULL,
	    FALSE,
	    NULL,
	    NULL,
	    FALSE,
	    TRUE,
	    NULL,
	    (SELECT cte_address.street_id FROM cte_address LIMIT 1) as street_id,   
	    (SELECT cte_address.neighborhood_id FROM cte_address LIMIT 1) as neighborhood_id,  
	    (SELECT cte_address.city_id FROM cte_address LIMIT 1) as city_id,  
	    (SELECT cte_address.state_id FROM cte_address LIMIT 1) as state_id,
	    TRUE
	  WHERE 
	    NOT EXISTS (SELECT 1 FROM document_document doc WHERE doc.hash = document__hash)
	  LIMIT 1;
END;
$BODY$
LANGUAGE plpgsql;