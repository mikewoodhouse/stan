SELECT
  pl.player_id
, pl.name
, SUM(pe.matches) AS appearances
, MIN(pe.year)    AS from_year
, MAX(pe.year)    AS to_year
FROM
  player_lookup pl
  JOIN performances pe ON pe.player_id = pl.player_id
GROUP BY
  pl.player_id
, pl.name
HAVING
  SUM(pe.matches) >= ':min_apps'
ORDER BY
  3 DESC