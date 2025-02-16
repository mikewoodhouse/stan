from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass

from app.config import config

SQL = """

"""


@dataclass
class AllTimeBowling:
    player_id: int
    name: str
    from_yr: int
    to_yr: int
    seasons: int

    @staticmethod
    def all(min_innings: int) -> list[AllTimeBowling]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                SQL,
                {
                    "min_innings": min_innings,
                },
            )
            return [AllTimeBowling(**row) for row in csr.fetchall()]

    @staticmethod
    def table_cols():
        return [{}]
