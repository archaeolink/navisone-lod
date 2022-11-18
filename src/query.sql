CREATE VIEW lod.lod_objects AS
SELECT o.id, o.name as label, lost.name as type, i.filename as img
FROM e22_object as o, lut_objectspecialtype as lost, d9_image as i
WHERE o.fk_id_objectspecialtype = lost.id
AND o.fk_id_image_primary = i.id
ORDER BY id;

CREATE VIEW lod.lod_object_metadata AS
SELECT ct_objectkeyword.fk_id_object, ct_objectkeyword.fk_id_metaindex, lut_objectkeywordtype.name, e55_keyword.en, e55_keyword.de
FROM ct_objectkeyword, lut_objectkeywordtype, e55_keyword
WHERE ct_objectkeyword.fk_id_type = lut_objectkeywordtype.id 
AND ct_objectkeyword.fk_id_metaindex = e55_keyword.id
AND lut_objectkeywordtype.name IN ('culture', 'material', 'technique', 'objecttype')
ORDER BY fk_id_object ASC;