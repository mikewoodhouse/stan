from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass

from app.config import config

SQL = """
WITH player_lookup AS
(
    SELECT id AS player_id
    , surname ||
        CASE
            WHEN length(firstname) > 0 THEN ', ' || firstname
            ELSE
                CASE
                    WHEN length(initial) > 0 THEN ', ' || initial
                    ELSE ''
                END
        END AS name
    FROM players
)
, perf_plus AS (
    SELECT
        *
    ,	overs * 6 + balls AS ballsbowled
    FROM performances
)
SELECT
  p.player_id
, p.name
, Min(perf.year) from_yr
, Max(perf.year) to_yr
, Count(*) AS seasons
, Sum(perf.ballsbowled) AS ballsbowled
, Sum(perf.maidens) AS maidens
, Sum(perf.wickets) AS wickets
, Sum(perf.runs) AS runs_conceded
, Cast(Sum(perf.runs) AS FLOAT) / Sum(perf.wickets) AS bowlave
, Cast(Sum(perf.ballsbowled) AS FLOAT) / Sum(perf.wickets) as strike_rate
, 6.0 * Sum(perf.runs) / Sum(perf.ballsbowled) AS econ
FROM
    perf_plus perf
    JOIN
    player_lookup p ON p.player_id = perf.player_id
WHERE perf.overs + perf.balls > 0
GROUP BY
  p.player_id
, p.name
HAVING
  Sum(perf.wickets) >= :min_wickets
ORDER BY bowlave
"""


@dataclass
class AllTimeBowling:
    player_id: int
    name: str
    from_yr: int
    to_yr: int
    seasons: int
    ballsbowled: int
    wickets: int
    maidens: int
    runs_conceded: int
    bowlave: float
    strike_rate: float
    econ: float

    @staticmethod
    def all(min_wickets: int) -> list[AllTimeBowling]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                SQL,
                {
                    "min_wickets": min_wickets,
                },
            )
            return [AllTimeBowling(**row) for row in csr.fetchall()]

    @staticmethod
    def table_cols():
        return [{}]
