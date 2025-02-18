WITH
    pt AS (
        SELECT
            *
          , ROW_NUMBER() OVER (
                PARTITION BY
                    YEAR
                  , wicket
                ORDER BY
                    total DESC
            ) AS rownum
        FROM
            partnerships
        WHERE
            YEAR = ':year'
    )
SELECT
    pt.*
  , b1.name AS bat1_name
  , b2.name AS bat2_name
FROM
    pt
    JOIN player_lookup b1 ON b1.player_id = pt.bat1_id
    JOIN player_lookup b2 ON b2.player_id = pt.bat2_id
WHERE
    total >= ':min_total'
    OR rownum = 1
ORDER BY
    wicket
  , total DESC