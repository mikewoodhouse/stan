import sqlite3

from nicegui import ui
from app.types import Captain
from app.pages.sidebar_menu import sidebar


def show_captains(db: sqlite3.Connection):
    sidebar()

    rows = Captain.all(db)

    with ui.column():
        ui.table(rows=rows).props("dense")
