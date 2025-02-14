from dataclasses import dataclass, asdict
import sqlite3
from contextlib import closing
from app.config import config


@dataclass(kw_only=True)
class Captain:
    player_id: int = -1
    code: str
    year: int = -1
    matches: int
    won: int
    lost: int
    drawn: int
    nodecision: int
    tied: int

    @classmethod
    def all(cls, db: sqlite3.Connection) -> list[dict]:
        with closing(db.cursor()) as csr:
            csr.execute(
                """
            SELECT
                code
            ,   SUM(matches) as matches
            ,   SUM(won) AS won
            ,   SUM(lost) AS lost
            ,   SUM(drawn) AS drawn
            ,   SUM(nodecision) AS nodecision
            ,   SUM(tied) AS tied
            FROM captains
            GROUP BY code
            HAVING SUM(matches) >= :min_captained
            ORDER BY 2 DESC
            """,
                {"min_captained": config.MIN_CAPTAINED},
            )
            rows = [Captain(**row) for row in csr.fetchall()]
            return [asdict(row) for row in rows]
