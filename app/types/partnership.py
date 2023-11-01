from dataclasses import dataclass
from datetime import date

from dataclass_csv import dateformat


@dataclass(kw_only=True)
@dateformat(r"%Y-%m-%d %H:%M:%S")
class Partnership:
    year: int
    wicket: int
    date: date
    total: int
    undefeated: bool
    bat1: str
    bat1score: int
    bat1notout: bool
    bat2: str
    bat2score: int
    bat2notout: bool
    opp: str
    bat1_id: int = -1
    bat2_id: int = -1
