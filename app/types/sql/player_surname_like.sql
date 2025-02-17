SELECT
    *
FROM
    players
WHERE
    surname LIKE ':surname_like'
ORDER BY
    surname
  , initial