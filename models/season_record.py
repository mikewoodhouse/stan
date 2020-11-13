from datetime import date
from typing import NamedTuple
import csv


class SeasonRecord(NamedTuple):
    year: int
    club: str
    runsscored: int
    wicketslost: int
    highest: int
    highestwkts: int
    highestdate: date
    highestopps: str
    lowest: int
    lowestwkts: int
    lowestdate: date
    lowestopps: str
    byes: int
    legbyes: int
    wides: int
    noballs: int
    ballsbowled: int
    ballsreceived: int