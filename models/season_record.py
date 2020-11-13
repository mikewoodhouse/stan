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

    @staticmethod
    def all():

        def fix_up_field(s):
            if s.isnumeric():
                return int(s)
            elif " 00:00:00" in s:
                return date(int(s[0:4]), int(s[5:7]), int(s[8:10]))
            else:
                return s

        def fix_up(row):
            return {k: fix_up_field(v) for k, v in row.items()}

        with open("SeasonRecord.csv") as f:
            reader = csv.DictReader(f, delimiter=',', quotechar='"')
            return [SeasonRecord(*fix_up(row).values()) for row in reader]

    @staticmethod
    def get(year):
        rows = {s.club: s for s in SeasonRecord.all() if s.year == year}
        return [rows['TCC'], rows['Opp']]
