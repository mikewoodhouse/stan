SELECT
    p.player_id
  , p.name
  , h.*
FROM
    hundred_plus h
    JOIN player_lookup p ON h.player_id = p.player_id
ORDER BY
    h.date