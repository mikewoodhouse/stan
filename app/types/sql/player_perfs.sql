SELECT
    f.*
  , p.name
FROM
    performances f
    JOIN player_lookup p ON p.player_id = f.player_id
WHERE
    f.player_id = ':player_id'
ORDER BY
    f.year