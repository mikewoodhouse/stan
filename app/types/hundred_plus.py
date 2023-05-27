from dataclasses import dataclass
from datetime import date
from typing import Optional

from dataclass_csv import dateformat

from app.types import Player


@dataclass(kw_only=True)
@dateformat(r"%Y-%m-%d %H:%M:%S")
class HundredPlus:
    id: int = -1
    player_id: int = -1
    year: int
    code: str
    date: date
    score: int
    notout: bool
    opponents: str
    minutes: Optional[int] = None

    def row_dict(self, players: dict) -> dict:
        player: Player = players[self.player_id]
        name = player.name
        return {
            "player_id": self.player_id,
            "name": name,
            "score": f"{self.score}{'*' if self.notout else ''}",
            "opponents": self.opponents,
            "date": self.date,
        }
