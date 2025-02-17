from contextlib import closing
from dataclasses import dataclass

from dataclasses_json import Undefined, dataclass_json

from app.config import config
from app.utils import player_name, sql_query


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
                sql_query("captain"),
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
                sql_query("captain_for_player"),
                {"player_id": player_id},
            )
            rows = [dict(row) for row in csr.fetchall()]
            for row in rows:
                row["won_pct"] = f"{row['won'] / row['matches']:7.02%}"
                row["not_lost_pct"] = f"{(row['matches'] - row['lost']) / row['matches']:7.02%}"
            return rows
