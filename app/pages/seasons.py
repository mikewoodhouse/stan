import sqlite3
from contextlib import closing

from nicegui import ui

from app.types.classes import Performance, Player


def show_season(db: sqlite3.Connection, year: int) -> None:
    # season
    # season_records
    # batting avgs
    # bowling avgs

