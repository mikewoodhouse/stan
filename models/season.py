from typing import NamedTuple
import csv
from .csv_utils import fix_up


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
        with open("Season.csv") as f:
            reader = csv.DictReader(f, delimiter=',', quotechar='"')
            return [Season(*fix_up(row).values()) for row in reader]
