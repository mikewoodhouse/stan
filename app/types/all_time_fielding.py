from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass

from app.config import config
from app.utils import sql_query


@dataclass
class AllTimeFielding:
    player_id: int
    name: str
    caught: int
    caughtwkt: int
    stumped: int

    @staticmethod
    def all(min_innings: int) -> list[AllTimeFielding]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                sql_query("fielding"),
                {
                    "min_innings": min_innings,
                },
            )
            return [AllTimeFielding(**row) for row in csr.fetchall()]
