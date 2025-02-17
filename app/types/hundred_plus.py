from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass
from datetime import date as pydate
from typing import Optional

from dataclass_csv import dateformat

import app.types
from app.config import config


@dataclass(kw_only=True)
@dateformat(r"%Y-%m-%d %H:%M:%S")
class HundredPlus:
    id: int = -1
    player_id: int = -1
    year: int
    code: str
    date: pydate
    score: int
    notout: bool
    opponents: str
    minutes: Optional[int] = None

    def row_dict(self, players: dict) -> dict:
        player: app.types.Player = players[self.player_id]
        name = player.name
        return {
            "player_id": self.player_id,
            "name": name,
            "score": f"{self.score}{'*' if self.notout else ''}",
            "opponents": self.opponents,
            "date": self.date,
        }

    @classmethod
    def all(cls) -> list[HundredPlus]:
        with closing(config.db.cursor()) as csr:
            csr.execute("SELECT * FROM hundred_plus ORDER BY date")
            rows = list(csr.fetchall())
            return [HundredPlus(**row) for row in rows]
