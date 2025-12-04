SELECT
  f.player_id
, p.name
, MIN(f.year) AS from_year
, MAX(f.year) AS to_year
FROM
  player_lookup p
  JOIN performances f ON f.player_id = p.player_id
WHERE
  p.surname LIKE ':starts_with'
GROUP BY
  p.name
, f.player_id
ORDER BY
  p.name