from datetime import date
from typing import NamedTuple
import csv


class Season(NamedTuple):
    year: int
    played: int
    won: int
    lost: int
    drawn: int
    tied: int
    nr: int
    max_games: int

    def get(year):
        for_year = list(filter(lambda s: s.year == year, Season.all()))
        return for_year[0]

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

        with open("Season.csv") as f:
            reader = csv.DictReader(f, delimiter=',', quotechar='"')
            return [Season(*fix_up(row).values()) for row in reader]
