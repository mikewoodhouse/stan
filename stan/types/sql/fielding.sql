SELECT
  f.player_id
, p.name
, SUM(f.caught)    AS caught
, SUM(f.caughtwkt) AS caughtwkt
, SUM(f.stumped)   AS stumped
FROM
  performances f
  JOIN player_lookup p ON p.player_id = f.player_id
GROUP BY
  f.player_id
, p.name
HAVING
  SUM(f.caught) + SUM(f.caughtwkt) + SUM(f.stumped) > 0