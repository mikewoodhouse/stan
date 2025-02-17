SELECT
    c.player_id
  , p.surname
  , p.firstname
  , p.initial
  , SUM(c.matches)    AS matches
  , SUM(c.won)        AS won
  , SUM(c.lost)       AS lost
  , SUM(c.drawn)      AS drawn
  , SUM(c.nodecision) AS nodecision
  , SUM(c.tied)       AS tied
FROM
    captains c
    JOIN players p ON p.id = c.player_id
GROUP BY
    c.player_id
  , p.surname
  , p.firstname
  , p.initial
HAVING
    SUM(matches) >= ':min_captained'
ORDER BY
    5 DESC