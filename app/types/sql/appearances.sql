SELECT
    pl.id           AS player_id
  , pl.surname
  , pl.initial
  , pl.firstname
  , SUM(pe.matches) AS appearances
  , MIN(pe.year)    AS from_year
  , MAX(pe.year)    AS to_year
FROM
    players pl
    JOIN performances pe ON pe.player_id = pl.id
GROUP BY
    pl.id
  , pl.surname
  , pl.initial
  , pl.firstname
HAVING
    SUM(pe.matches) >= ':min_apps'
ORDER BY
    5 DESC