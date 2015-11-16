select revisions from contact_phone where id = 1;
update contact_phone set revisions = NULL where id = 1;
SELECT EXTRACT(EPOCH FROM updated_at) from contact_phone where id = 1;


update 
	contact_phone as cp 
	set revisions = (
			SELECT 
				json_build_array(
					row_to_json(( SELECT _struct FROM 
										(
											SELECT 
												EXTRACT(EPOCH FROM cp.updated_at) as id,
												row_to_json((SELECT _row FROM (SELECT id, type, areacode, number, address_id, carrier_id) _row )) as revision
										) _struct
									))
				)
			);
	 
	 
	 
	 SELECT json_build_array (
	 			(SELECT 

					json_build_object(
						'id', EXTRACT(EPOCH FROM cp.updated_at),
						'revision', (select row_to_json(contact_phone) from contact_phone where id = cp.id)
					)
				as agg from contact_phone  as cp where cp.id  = 1),
				(SELECT 

					json_build_object(
						'id', EXTRACT(EPOCH FROM cp.updated_at),
						'revision', (select row_to_json(contact_phone) from contact_phone where id = cp.id)
					)
				as agg from contact_phone  as cp where cp.id  = 2)	
			)