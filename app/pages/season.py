import sqlite3
from contextlib import closing

from nicegui import ui
from dataclasses import asdict
from app.types.classes import Season, SeasonRecord


def get_season(db: sqlite3.Connection, year: int) -> Season:
    with closing(db.cursor()) as csr:
        csr.execute("SELECT * FROM seasons WHERE year = :year", {"year": year})
        row: dict = csr.fetchone()
        return Season(**row)


def show_season(db: sqlite3.Connection, year: int) -> None:
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"{year} Season").style("color: gold")
    season = get_season(db, year)
    with ui.row():
        cols = [
            {"name": "played", "label": "P", "field": "played"},
            {"name": "won", "label": "W", "field": "won"},
            {"name": "lost", "label": "L", "field": "lost"},
            {"name": "drawn", "label": "D", "field": "drawn"},
            {"name": "tied", "label": "T", "field": "tied"},
            {"name": "noresult", "label": "N/R", "field": "noresult"},
        ]
        ui.table(rows=[asdict(season)], columns=cols).props("dense")
    # season
    # season_records
    # batting avgs
    # bowling avgs

    ...
