from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass

from app.config import config

SQL = """

"""


@dataclass
class AllTimeFielding:
    player_id: int
    name: str
    from_yr: int
    to_yr: int
    seasons: int

    @staticmethod
    def all(min_innings: int) -> list[AllTimeFielding]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                SQL,
                {
                    "min_innings": min_innings,
                },
            )
            return [AllTimeFielding(**row) for row in csr.fetchall()]

    @staticmethod
    def table_cols():
        return [{}]
