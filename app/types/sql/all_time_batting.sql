SELECT
    p.player_id
  , p.name
  , MIN(perf.year) from_yr
  , MAX(perf.year) to_yr
  , SUM(
        CASE perf.innings
            WHEN 0 THEN 0
            ELSE 1
        END
    ) seasons
  , SUM(perf.matches) matches
  , SUM(perf.innings) innings
  , SUM(perf.notout) notout
  , (
        SELECT
            MAX(pf.highest)
        FROM
            performances pf
        WHERE
            pf.player_id = p.player_id
    ) || CASE (
            SELECT
                MAX(f.highestnotout)
            FROM
                performances f
            WHERE
                f.player_id = p.player_id
                AND f.highest = (
                    SELECT
                        MAX(ff.highest)
                    FROM
                        performances ff
                    WHERE
                        ff.player_id = p.player_id
                )
        )
        WHEN 1 THEN '*'
        ELSE ''
    END high_score
  , SUM(perf.runsscored) runsscored
  , CASE SUM(perf.innings)
        WHEN SUM(perf.notout) THEN 0.0
        ELSE SUM(CAST(perf.runsscored AS REAL)) / (SUM(perf.innings) - SUM(perf.notout))
    END batave
  , SUM(perf.fours) fours
  , SUM(perf.sixes) sixes
  , SUM(perf.fifties) fifties
  , SUM(perf.hundreds) hundreds
FROM
    performances perf
    JOIN player_lookup p ON p.player_id = perf.player_id
GROUP BY
    p.player_id
  , p.name
HAVING
    SUM(perf.innings) >= ':min_innings'
ORDER BY
    batave DESC