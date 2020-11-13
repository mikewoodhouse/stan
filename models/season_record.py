from datetime import date
from typing import NamedTuple
import csv
from .csv_utils import fix_up


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

    @staticmethod
    def all():
        with open("SeasonRecord.csv") as f:
            reader = csv.DictReader(f, delimiter=',', quotechar='"')
            return [SeasonRecord(*fix_up(row).values()) for row in reader]

    @staticmethod
    def get(year):
        rows = {s.club: s for s in SeasonRecord.all() if s.year == year}
        return [rows['TCC'], rows['Opp']]
