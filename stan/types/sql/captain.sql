SELECT
  c.player_id
, p.name
, SUM(c.matches)    AS matches
, SUM(c.won)        AS won
, SUM(c.lost)       AS lost
, SUM(c.drawn)      AS drawn
, SUM(c.nodecision) AS nodecision
, SUM(c.tied)       AS tied
FROM
  captains c
  JOIN player_lookup p ON p.player_id = c.player_id
GROUP BY
  c.player_id
, p.name
HAVING
  SUM(matches) >= ':min_captained'
ORDER BY
  SUM(c.matches) DESC