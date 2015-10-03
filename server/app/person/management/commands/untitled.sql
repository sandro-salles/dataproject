CREATE OR REPLACE FUNCTION get_or_create_person_with_dependencies(
	person__nature varchar,    
	person__name varchar,
	person_ctype_id integer,

	document__number varchar,	

	phone__hash integer,
	phone__carrier_id integer,
	phone__type varchar,
	phone__area_code varchar, 
    phone__number varchar,
    phone_ctype_id integer,

    address__hash integer,
    address__address varchar,
    address__number varchar,
    address__complement varchar,
    address__neighborhood__name varchar,
    address__zipcode varchar,
    address__city__name varchar,
    address__state__abbreviation varchar,
    address_ctype_id integer
)
  RETURNS json AS
$BODY$
DECLARE
    person_id integer;
    person_is_new boolean DEFAULT true;

    document_id integer;
    document_is_new boolean DEFAULT true;

    phone_id integer;
    phone_is_new boolean DEFAULT true;
    phone_relation_is_new boolean DEFAULT true;

    address_id integer;
    address_is_new boolean DEFAULT true;
    address_relation_is_new boolean DEFAULT true;

    results json;
BEGIN
  	IF person__nature = 'F' THEN

	  	-- Start checking for existing person for a given document number

	  	SELECT INTO 
	  		person_id, document_id 
	  			doc.id, person.id 
	  				FROM 
	  					document_cpf doc 
					INNER JOIN 
						person_person person ON (person.id = doc.person_id) 
					WHERE 
						number = document__number;


  		IF document_id IS NOT NULL THEN -- A person exists for this document number
  			document_is_new = false;
  			person_is_new = false;

  			-- MUST TREAT DIRTY PERSON DATA HERE

		ELSE 

			-- ITS A NEW PERSON/DOCUMENT
			-- INSERT THE NEW PERSON TO PERSONS TABLE

			SELECT INTO 
				person_id
					id
						FROM 	(
									INSERT INTO 
										person_person
											(created_at, updated_at, is_dirty, name, polymorphic_ctype_id) 
										VALUES
											(NOW(), NOW(), false, person__name, person_ctype_id)
										RETURNING id;
								);

				-- INSERT THE POINTER TO PHYSICALPERSONS TABLE

				INSERT INTO
					person_physicalperson
						(person_ptr_id)
					VALUES
						(person_id);


			-- INSERT THE NEW PERSON CPF DOCUMENT

			SELECT INTO 
				document_id 
					id
						FROM 	(
									INSERT INTO 
							    		document_cpf 
							      			(created_at, updated_at, is_dirty, number, person_id) 
							    		VALUES
							      			(NOW(), NOW(), false, document__number, person_id)
							    		RETURNING id 
		    					);	
  		END IF;

  		SELECT INTO 
  			phone_id, phone_relation_is_new
	  			cphone.contact_ptr_id,  CASE WHEN cphonep.id IS NULL THEN true ELSE false END
	  				FROM 
	  					contact_phone cphone
					LEFT JOIN
						contact_contact_persons cphonep ON (cphonep.person_id = person_id AND cphonep.contact_id = cphone.contact_ptr_id)
					WHERE 
						hash = phone__hash;

		IF phone_id IS NOT NULL THEN  -- this phone already exists
			phone_is_new = false
		ELSE

			-- ITS A NEW PHONE NUMBER
			-- INSERT THE NEW PHONE NUMBER TO CONTACTS TABLE

			SELECT INTO 
				phone_id 
					id
						FROM 	(
									INSERT INTO 
							    		contact_contact 
							      			(created_at, updated_at, is_dirty, polymorphic_ctype_id) 
							    		VALUES
							      			(NOW(), NOW(), false, phone_ctype_id)
							    		RETURNING id 
		    					);

				-- INSERT THE POINTER TO CONTACT PHONES TABLE

				INSERT INTO
					contact_phone
						(contact_ptr_id, type, area_code, number, hash, carrier_id)
					VALUES
						(phone_id, phone__type, phone__area_code, phone__number, phone__hash, phone__carrier_id);

		END IF:

		IF phone_relation_is_new THEN

			INSERT INTO
				contact_contact_persons
					(contact_id, person_id)
				VALUES
					(phone_id, person_id)

		END IF

		

  	END IF;

  SELECT row_to_json(r) into results from (select log_nu_sequencial, log_no from log_logradouro where cep = '04134070' limit 1) r;
  RETURN results;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;