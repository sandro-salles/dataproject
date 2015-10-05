WITH 
  cte_phone as  (
    SELECT 
      phone.contact_ptr_id as phone_id, 
      phone.carrier_id as carrier_id
    FROM 
      contact_phone phone
    WHERE 
      phone.hash = {phone__hash} 
  ),
  cte_address as (
    SELECT 
      address.contact_ptr_id as address_id,
      street.log_nu_sequencial as street_id,
      neighborhood.bai_nu_sequencial as neighborhood_id,
      city.loc_nu_sequencial as city_id,
      state.ufe_sg as state_id
    FROM 
      contact_address address
    INNER JOIN
      log_logradouro street
        ON (street.log_nu_sequencial = address.street_id)
    INNER JOIN
      log_bairro neighborhood
        ON (neighborhood.bai_nu_sequencial = street.bai_nu_sequencial_ini)
    INNER JOIN
      log_localidade city
      ON (city.loc_nu_sequencial = neighborhood.loc_nu_sequencial)
    INNER JOIN
      log_localidade state
      ON (state.ufe_sg = city.ufe_sg)
    WHERE 
      address.hash = {address__hash} 
    UNION ALL
      SELECT 
        NULL,
        street.log_nu_sequencial as street_id,
        neighborhood.bai_nu_sequencial as neighborhood_id,
        city.loc_nu_sequencial as city_id,
        state.ufe_sg as state_id
      FROM 
        log_logradouro street
      INNER JOIN
        log_bairro neighborhood
          ON (neighborhood.bai_nu_sequencial = street.bai_nu_sequencial_ini)
      INNER JOIN
        log_localidade city
        ON (city.loc_nu_sequencial = neighborhood.loc_nu_sequencial)
      INNER JOIN
        log_localidade state
        ON (state.ufe_sg = city.ufe_sg)
      WHERE 
        NOT EXISTS (SELECT 1 FROM contact_address address WHERE address.hash = {address__hash}) 
        AND street.cep = '{address__zipcode}'
  )
SELECT 
  person.id as person_id,
  (CASE WHEN person.id IS NOT NULL AND person.name <> '{person__name}' THEN true ELSE false END) as person_is_dirty,
  doc.id as document_id,   
  (SELECT phone_id FROM cte_phone LIMIT 1) as phone_id,
  (SELECT (CASE WHEN carrier_id IS NOT NULL AND carrier_id <> {phone__carrier_id} THEN true ELSE false END) FROM cte_phone LIMIT 1) as phone_carrier_has_changed,
  (CASE WHEN cphonep.id IS NULL THEN true ELSE false END) as phone_relation_is_new,
  (SELECT address_id FROM cte_address LIMIT 1) as address_id,  
  (SELECT street_id FROM cte_address LIMIT 1) as street_id,   
  (SELECT neighborhood_id FROM cte_address LIMIT 1) as neighborhood_id,  
  (SELECT city_id FROM cte_address LIMIT 1) as city_id,  
  (SELECT state_id FROM cte_address LIMIT 1) as state_id,  
  (CASE WHEN caddressp.id IS NULL THEN true ELSE false END) as address_relation_is_new
FROM 
  document_cpf doc 
INNER JOIN 
  person_person person 
    ON (person.id = doc.person_id)
LEFT OUTER JOIN
  contact_contact_persons cphonep
    ON (
      cphonep.person_id = person.id 
      AND cphonep.contact_id IN (SELECT phone_id FROM cte_phone LIMIT 1)
      AND (SELECT phone_id FROM cte_phone LIMIT 1) IS NOT NULL
    )
LEFT OUTER JOIN
  contact_contact_persons caddressp
    ON (
      caddressp.person_id = person.id 
      AND caddressp.contact_id IN (SELECT address_id FROM cte_address LIMIT 1)
      AND (SELECT address_id FROM cte_address LIMIT 1) IS NOT NULL   )
WHERE 
  doc.number = '{document__number}'
UNION ALL
  SELECT 
    NULL,
    FALSE,
    NULL,
    NULL,
    FALSE,
    TRUE,
    NULL,
    (SELECT street_id FROM cte_address LIMIT 1) as street_id,   
    (SELECT neighborhood_id FROM cte_address LIMIT 1) as neighborhood_id,  
    (SELECT city_id FROM cte_address LIMIT 1) as city_id,  
    (SELECT state_id FROM cte_address LIMIT 1) as state_id,
    TRUE
  WHERE 
    NOT EXISTS (SELECT 1 FROM document_cpf doc WHERE doc.number = '{document__number}');