SELECT
    pt.*
  , b1.name AS bat1_name
  , b2.name AS bat2_name
FROM
    partnerships pt
    JOIN player_lookup b1 ON b1.player_id = pt.bat1_id
    JOIN player_lookup b2 ON b2.player_id = pt.bat2_id
WHERE
    wicket = ':wicket'
ORDER BY
    wicket
  , total DESC