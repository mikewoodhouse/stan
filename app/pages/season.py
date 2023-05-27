import sqlite3
from contextlib import closing
from dataclasses import asdict

from nicegui import ui

from app.types import Season, SeasonRecord


def get_season(db: sqlite3.Connection, year: int) -> Season:
    with closing(db.cursor()) as csr:
        csr.execute("SELECT * FROM seasons WHERE year = :year", {"year": year})
        row: dict = csr.fetchone()
        return Season(**row)


def get_season_records(db: sqlite3.Connection, year: int) -> list[SeasonRecord]:
    with closing(db.cursor()) as csr:
        csr.execute("SELECT * FROM season_records WHERE year = :year", {"year": year})
        rows: list[dict] = csr.fetchall()
        return [SeasonRecord(**row) for row in rows]


def show_season(db: sqlite3.Connection, year: int) -> None:
    with ui.header(elevated=True).style("background-color: maroon"):
        ui.label(f"{year} Season").style("color: gold")
    with ui.row():
        cols = [
            {"name": "played", "label": "P", "field": "played"},
            {"name": "won", "label": "W", "field": "won"},
            {"name": "lost", "label": "L", "field": "lost"},
            {"name": "drawn", "label": "D", "field": "drawn"},
            {"name": "tied", "label": "T", "field": "tied"},
            {"name": "noresult", "label": "N/R", "field": "noresult"},
        ]
        season = get_season(db, year)
        ui.table(rows=[asdict(season)], columns=cols).props("dense")
    with ui.row():
        cols = [
            {"name": "club", "label": "club", "field": "club"},
            {"name": "runsscored", "label": "runsscored", "field": "runsscored"},
            {"name": "wicketslost", "label": "wicketslost", "field": "wicketslost"},
            {"name": "highest", "label": "highest", "field": "highest"},
            {"name": "highestwkts", "label": "highestwkts", "field": "highestwkts"},
            {"name": "highestdate", "label": "highestdate", "field": "highestdate"},
            {"name": "highestopps", "label": "highestopps", "field": "highestopps"},
            {"name": "lowest", "label": "lowest", "field": "lowest"},
            {"name": "lowestwkts", "label": "lowestwkts", "field": "lowestwkts"},
            {"name": "lowestdate", "label": "lowestdate", "field": "lowestdate"},
            {"name": "lowestopps", "label": "lowestopps", "field": "lowestopps"},
            {"name": "byes", "label": "byes", "field": "byes"},
            {"name": "legbyes", "label": "legbyes", "field": "legbyes"},
            {"name": "wides", "label": "wides", "field": "wides"},
            {"name": "noballs", "label": "noballs", "field": "noballs"},
            {"name": "overs_bowled", "label": "overs_bowled", "field": "overs_bowled"},
            {
                "name": "overs_faced",
                "label": "overs_faced",
                "field": "overs_faced",
            },
        ]
        records = [row.row_dict() for row in get_season_records(db, year)]
        ui.table(rows=records, columns=cols).props("dense")
        # batting avgs
        # bowling avgs
