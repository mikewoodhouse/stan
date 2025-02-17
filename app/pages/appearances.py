from nicegui import ui

from app.config import config
from app.types import Performance
from app.utils import add_slot_to_table, coldef, page_header

from .sidebar_menu import sidebar

COLS = [
    coldef("player_name", "Name", align="left"),
    coldef("appearances", "Apps"),
    coldef("from_year", "From"),
    coldef("to_year", "To"),
]


def show_appearances():
    page_header("Career Appearances")

    sidebar()

    rows = Performance.career_appearances()
    with ui.row():
        with ui.column():
            ui.label(f"All players with a minimum of {config.MIN_APPS} appearances")
            with ui.table(rows=rows, columns=COLS).props("dense") as table:
                add_slot_to_table(table, "player_name", "players", "player_id")
