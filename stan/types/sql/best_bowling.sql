WITH
    mb AS (
        SELECT
            CAST(player_id AS INTEGER)                              AS player_id
          , CAST(strftime ('%Y', datetime (match_date)) AS INTEGER) AS YEAR
          , CAST(wickets AS INTEGER)                                AS wickets
          , CAST(runs_conceded AS INTEGER)                          AS runs
          , match_date
          , opp
        FROM
            match_bowling
    )
  , most_wickets AS (
        SELECT
            player_id
          , YEAR
          , MAX(wickets) AS wickets
        FROM
            mb
        WHERE
            player_id = ':player_id'
        GROUP BY
            player_id
          , YEAR
    )
  , bb AS (
        SELECT
            w.player_id
          , w.year
          , w.wickets
          , MIN(mb.runs) AS runs
        FROM
            most_wickets w
            JOIN mb ON mb.player_id = w.player_id
            AND mb.year = w.year
            AND w.wickets = mb.wickets
        GROUP BY
            w.player_id
          , w.year
          , w.wickets
    )
  , maxed AS (
        SELECT
            player_id
          , YEAR
          , wkts               AS wickets
          , runs
          , wkts * 1000 - runs AS sort_key
        FROM
            best_bowling
        WHERE
            player_id = ':player_id'
            AND YEAR < 1997
    )
  , by_year AS (
        SELECT
            player_id
          , YEAR
          , MAX(sort_key) AS best
        FROM
            maxed
        GROUP BY
            player_id
          , YEAR
    )
SELECT
    bb.year
  , bb.wickets
  , bb.runs
  , bb.wickets * 1000 - bb.runs AS sort_key
FROM
    bb
    LEFT JOIN mb ON bb.player_id = mb.player_id
    AND bb.wickets = mb.wickets
    AND bb.runs = mb.runs
    AND bb.year = mb.year
UNION
SELECT
    x.year
  , x.wickets
  , x.runs
  , x.sort_key
FROM
    maxed x
    JOIN by_year y ON y.player_id = x.player_id
    AND y.year = x.year
    AND y.best = x.sort_key