from datetime import date
from typing import NamedTuple
import csv
from .csv_utils import fix_up


class Century(NamedTuple):
    year: int
    code: str
    date: date
    score: int
    notout: int
    opponents: str
    minutes: int

    def all():
        with open("HundredPlus.csv") as f:
            reader = csv.DictReader(f, delimiter=',', quotechar='"')
            return [Century(*fix_up(row).values()) for row in reader]
