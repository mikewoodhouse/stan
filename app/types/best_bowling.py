from dataclasses import dataclass
from datetime import date


@dataclass
class BestBowling:
    player_id: int
    year: int
    code: str
    date: date
    inns: int
    wkts: int
    runs: int
    opp: str
