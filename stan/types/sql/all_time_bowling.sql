WITH
    perf_plus AS (
        SELECT
            *
          , overs * 6 + balls AS ballsbowled
        FROM
            performances
    )
SELECT
    p.player_id
  , p.name
  , MIN(perf.year)                                           from_yr
  , MAX(perf.year)                                           to_yr
  , COUNT(*)                                                 AS seasons
  , SUM(perf.ballsbowled)                                    AS ballsbowled
  , SUM(perf.maidens)                                        AS maidens
  , SUM(perf.wickets)                                        AS wickets
  , SUM(perf.runs)                                           AS runs_conceded
  , CAST(SUM(perf.runs) AS FLOAT) / SUM(perf.wickets)        AS bowlave
  , CAST(SUM(perf.ballsbowled) AS FLOAT) / SUM(perf.wickets) AS strike_rate
  , 6.0 * SUM(perf.runs) / SUM(perf.ballsbowled)             AS econ
FROM
    perf_plus perf
    JOIN player_lookup p ON p.player_id = perf.player_id
WHERE
    perf.overs + perf.balls > 0
GROUP BY
    p.player_id
  , p.name
HAVING
    SUM(perf.wickets) >= ':min_wickets'
ORDER BY
    bowlave