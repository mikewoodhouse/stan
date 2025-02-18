from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass
from datetime import date as pydate
from typing import Optional

from dataclass_csv import dateformat

from app.config import config
from app.utils import sql_query


@dataclass(kw_only=True)
@dateformat(r"%Y-%m-%d %H:%M:%S")
class HundredPlus:
    id: int = -1
    player_id: int = -1
    name: str = ""
    year: int
    code: str
    date: pydate
    score: int
    notout: bool
    opponents: str
    minutes: Optional[int] = None

    def row_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "score": f"{self.score}{'*' if self.notout else ''}",
            "opponents": self.opponents,
            "date": self.date,
        }

    @classmethod
    def all(cls) -> list[HundredPlus]:
        with closing(config.db.cursor()) as csr:
            csr.execute(sql_query("hundreds"))
            rows = list(csr.fetchall())
            return [HundredPlus(**row) for row in rows]
