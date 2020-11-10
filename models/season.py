from typing import NamedTuple


class Season(NamedTuple):
    year: int
    played: int
    won: int
    lost: int
    drawn: int
    tied: int
    nr: int
    max_games: int
