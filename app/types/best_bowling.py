from dataclasses import dataclass
from datetime import date as pydate

from dataclass_csv import dateformat


@dataclass(kw_only=True)
@dateformat(r"%Y-%m-%d %H:%M:%S")
class BestBowling:
    player_id: int = -1
    year: int = -1
    code: str = ""
    date: pydate
    inns: int
    wkts: int
    runs: int
    opp: str
