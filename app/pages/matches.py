import sqlite3
from dataclasses import asdict

from nicegui import ui

from app.types import Match

from .sidebar_menu import sidebar


def show_matches(db: sqlite3.Connection, year: int) -> None:
    sidebar()

    with ui.row():
        ui.label(f"{year} Matches")

    matches = Match.for_year(db, year)
    table_rows = [asdict(match) for match in matches]
    with ui.row():
        ui.table(rows=table_rows).props("dense")
