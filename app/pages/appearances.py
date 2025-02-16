from nicegui import ui

from app.config import config
from app.types import Performance
from app.utils import add_slot_to_table, page_header

from .sidebar_menu import sidebar

COLS = [
    {"name": "player_name", "label": "Name", "field": "player_name", "align": "left"},
    {"name": "apps", "label": "Apps", "field": "appearances", "align": "right"},
    {"name": "from_yr", "label": "From", "field": "from_year", "align": "center"},
    {"name": "to_yr", "label": "To", "field": "to_year", "align": "center"},
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
