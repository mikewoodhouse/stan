SELECT
    f.player_id
  , p.surname || CASE
        WHEN p.firstname != '' THEN ', ' || p.firstname
        ELSE CASE
            WHEN p.initial != '' THEN ', ' || p.initial
            ELSE ''
        END
    END AS name
  , MIN(f.year) AS from_year
  , MAX(f.year) AS to_year
FROM
    players p
    JOIN performances f ON f.player_id = p.id
WHERE
    p.surname LIKE ':starts_with'
GROUP BY
    p.surname
  , p.initial
  , p.firstname
  , f.player_id
ORDER BY
    p.surname
  , p.initial
  , p.firstname