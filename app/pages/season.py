import sqlite3
from dataclasses import asdict

from nicegui import ui

from app.types import Season, SeasonRecord


def show_season(db: sqlite3.Connection, year: int) -> None:
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"{year} Season").style("color: gold")
    with ui.row():
        season = Season.for_year(db, year)
        ui.table(rows=[asdict(season)], columns=Season.table_cols()).props("dense")
    with ui.row():
        records = [row.row_dict() for row in SeasonRecord.for_year(db, year)]
        ui.table(rows=records, columns=SeasonRecord.table_cols()).props("dense")
        # batting avgs
        # bowling avgs
