from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass

from app.config import config
from app.utils import sql_query


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
                sql_query("all_time_batting"),
                {
                    "min_innings": min_innings,
                },
            )
            return [AllTimeBatting(**row) for row in csr.fetchall()]

    @staticmethod
    def table_cols():
        return [{}]
