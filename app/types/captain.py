from contextlib import closing
from dataclasses import dataclass

from dataclasses_json import Undefined, dataclass_json

from app.config import config
from app.utils import player_name


@dataclass_json(undefined=Undefined.EXCLUDE)
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
    def all(cls) -> list[dict]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                """
            SELECT
                c.player_id
            ,   p.surname
            ,   p.firstname
            ,   p.initial
            ,   SUM(c.matches) as matches
            ,   SUM(c.won) AS won
            ,   SUM(c.lost) AS lost
            ,   SUM(c.drawn) AS drawn
            ,   SUM(c.nodecision) AS nodecision
            ,   SUM(c.tied) AS tied
            FROM captains c JOIN players p ON p.id = c.player_id
            GROUP BY
                c.player_id
            ,   p.surname
            ,   p.firstname
            ,   p.initial
            HAVING SUM(matches) >= :min_captained
            ORDER BY 5 DESC
            """,
                {"min_captained": config.MIN_CAPTAINED},
            )
            rows = [dict(row) for row in csr.fetchall()]
            for row in rows:
                row["player_name"] = player_name(row["firstname"], row["initial"], row["surname"])
                row["won_pct"] = f"{row["won"] / row["matches"]:7.02%}"
                row["not_lost_pct"] = f"{(row['matches'] - row['lost']) / row['matches']:7.02%}"
            return rows

    @classmethod
    def for_player(cls, player_id: int) -> list[dict]:
        with closing(config.db.cursor()) as csr:
            csr.execute(
                """
            SELECT
                *
            FROM captains
            WHERE player_id = :player_id
            ORDER BY year
            """,
                {"player_id": player_id},
            )
            rows = [dict(row) for row in csr.fetchall()]
            for row in rows:
                row["won_pct"] = f"{row['won'] / row['matches']:7.02%}"
                row["not_lost_pct"] = f"{(row['matches'] - row['lost']) / row['matches']:7.02%}"
            return rows
