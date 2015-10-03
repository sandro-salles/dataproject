WITH 
  cte_phone_id as  (
    SELECT 
      phone.contact_ptr_id as phone_id
    FROM 
      contact_phone phone
    WHERE 
      phone.hash = {phone__hash} 
  ),
  cte_address_id as (
    SELECT 
      address.contact_ptr_id as address_id
    FROM 
      contact_physicaladdress address
    WHERE 
      address.hash = {address__hash} 
  )
SELECT 
  person.id as person_id,
  (CASE WHEN person.id IS NOT NULL AND person.name <> '{person__name}' THEN true ELSE false END) as person_is_dirty,
  doc.id as document_id,   
  (SELECT phone_id FROM cte_phone_id LIMIT 1) as phone_id,
  (CASE WHEN cphonep.id IS NULL THEN true ELSE false END) as phone_relation_is_new,
  (SELECT address_id FROM cte_address_id LIMIT 1) as address_id,  
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
      AND cphonep.contact_id IN (SELECT phone_id FROM cte_phone_id LIMIT 1)
      AND (SELECT phone_id FROM cte_phone_id LIMIT 1) IS NOT NULL
    )
LEFT OUTER JOIN
  contact_contact_persons caddressp
    ON (
      caddressp.person_id = person.id 
      AND caddressp.contact_id IN (SELECT address_id FROM cte_address_id LIMIT 1)
      AND (SELECT address_id FROM cte_address_id LIMIT 1) IS NOT NULL   )
WHERE 
  doc.number = '{document__number}'
UNION ALL
  SELECT 
    NULL,
    FALSE,
    NULL,
    NULL,
    TRUE,
    NULL,
    TRUE
  WHERE 
    NOT EXISTS (SELECT 1 FROM document_cpf doc WHERE doc.number = '{document__number}');