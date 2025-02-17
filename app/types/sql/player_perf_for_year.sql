WITH
    batting_plus_year AS (
        SELECT
            *
          , CAST(STRFTIME ('%Y', DATETIME (match_date)) AS INTEGER) AS YEAR
        FROM
            match_batting
    )
SELECT
    ba.match_date
  , ba.opp
  , ba.captain
  , ba.kept_wicket   AS keeper
  , ba.position      AS bat_pos
  , ba.how_out
  , ba.runs          AS runs_scored
  , ba.fours
  , ba.sixes
  , bo.overs
  , bo.balls
  , bo.maidens
  , bo.runs_conceded
  , bo.wickets
  , ba.caught
  , ba.caught_wkt
  , ba.stumped
FROM
    batting_plus_year ba
    LEFT JOIN match_bowling bo ON ba.player_id = bo.player_id
    AND ba.match_id = bo.match_id
WHERE
    ba.player_id = ' :player_id'
    AND ba.year = ':year'
ORDER BY
    ba.match_date