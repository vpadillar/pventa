
CREATE OR REPLACE FUNCTION group_concat_iterate(_state numeric[], _value numeric)
  RETURNS numeric[] AS
$BODY$
  SELECT
    CASE
      WHEN $1 IS NULL THEN ARRAY[$2]
      ELSE $1 || $2
  END
$BODY$
  LANGUAGE SQL VOLATILE;

CREATE OR REPLACE FUNCTION group_concat_iterate(_state text[], _value text)
  RETURNS text[] AS
$BODY$
  SELECT
    CASE
      WHEN $1 IS NULL THEN ARRAY[$2]
      ELSE $1 || $2
  END
$BODY$
  LANGUAGE SQL VOLATILE;

CREATE OR REPLACE FUNCTION group_concat_finish(_state text[])
  RETURNS text AS
$BODY$
    SELECT array_to_string($1, ',')
$BODY$
  LANGUAGE SQL VOLATILE;

CREATE OR REPLACE FUNCTION group_concat_finish(_state numeric[])
  RETURNS text AS
$BODY$
    SELECT array_to_string($1::text[], ',')
$BODY$
  LANGUAGE SQL VOLATILE;

CREATE AGGREGATE group_concat(numeric) (SFUNC = group_concat_iterate, STYPE = numeric[], FINALFUNC = group_concat_finish);
CREATE AGGREGATE group_concat(text) (SFUNC = group_concat_iterate, STYPE = text[], FINALFUNC = group_concat_finish);