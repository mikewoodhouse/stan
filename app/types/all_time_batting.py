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
    SELECT
      p.player_id
    , p.name
    , Min(perf.year) from_yr
    , Max(perf.year) to_yr
    , Sum(CASE perf.innings WHEN 0 THEN 0 ELSE 1 END) seasons
    , Sum(perf.matches) matches
    , Sum(perf.innings) innings
    , Sum(perf.notout) notout
    , (SELECT Max(pf.highest) FROM performances pf WHERE pf.player_id = p.player_id) ||
      CASE (
          SELECT Max(f.highestnotout)
          FROM performances f
          WHERE f.player_id = p.player_id
          AND f.highest = (
              SELECT Max(ff.highest)
              FROM performances ff
              WHERE ff.player_id = p.player_id)
      ) WHEN 1 THEN '*' ELSE '' END high_score
    , Sum(perf.runsscored) runsscored
    , CASE Sum(perf.innings)
        WHEN Sum(perf.notout) THEN 0.0
        ELSE Sum(Cast(perf.runsscored AS REAL)) / (Sum(perf.innings) - Sum(perf.notout))
      END batave
    , Sum(perf.fours) fours
    , Sum(perf.sixes) sixes
    , Sum(perf.fifties) fifties
    , Sum(perf.hundreds) hundreds
    FROM
        performances perf
        JOIN
        player_lookup p ON p.player_id = perf.player_id
    GROUP BY
      p.player_id
    , p.name
    HAVING
      Sum(perf.innings) >= :min_innings
    ORDER BY batave DESC
"""


@dataclass
class AllTimeBatting:
    player_id: int
    name: str
    from_yr: int
    to_yr: int
    seasons: int
    matches: int
    innings: int
    notout: int
    high_score: str
    runsscored: int
    batave: float
    fours: int
    sixes: int
    fifties: int
    hundreds: int

    @staticmethod
    def all(min_innings: int) -> list[AllTimeBatting]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                SQL,
                {
                    "min_innings": min_innings,
                },
            )
            return [AllTimeBatting(**row) for row in csr.fetchall()]

    @staticmethod
    def table_cols():
        return [{}]
