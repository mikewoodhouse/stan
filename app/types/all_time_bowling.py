from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass

from app.config import config
from app.utils import sql_query


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
                sql_query("all_time_bowling"),
                {
                    "min_wickets": min_wickets,
                },
            )
            return [AllTimeBowling(**row) for row in csr.fetchall()]

    @staticmethod
    def table_cols():
        return [{}]
