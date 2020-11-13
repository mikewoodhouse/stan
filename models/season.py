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
        return Season(1949, 12, 4, 7, 1, 0, 0, 12)

    def all():
        with open("Season.csv") as f:
            reader = csv.reader(f, delimiter=',')
            next(reader)
            return [Season(*row) for row in reader]
