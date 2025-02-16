from nicegui import ui

from app.config import config
from app.pages.sidebar_menu import sidebar
from app.types import Captain
from app.utils import add_slot_to_table, page_header

COLS = [
    {"name": "player_name", "label": "Name", "field": "player_name", "align": "left", "sortable": True},
    {"name": "matches", "label": "Matches", "field": "matches", "sortable": True},
    {"name": "won", "label": "W", "field": "won", "sortable": True},
    {"name": "lost", "label": "L", "field": "lost", "sortable": True},
    {"name": "drawn", "label": "D", "field": "drawn", "sortable": True},
    {"name": "nodecision", "label": "N/D", "field": "nodecision", "sortable": True},
    {"name": "tied", "label": "T", "field": "tied", "sortable": True},
    {"name": "won_pct", "label": "Won", "field": "won_pct", "sortable": True},
    {"name": "not_lost_pct", "label": "Not Lost", "field": "not_lost_pct", "sortable": True},
]


def show_captains():
    page_header(f"Captains ({config.MIN_CAPTAINED} or more games)")

    sidebar()

    rows = Captain.all()

    with ui.column():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "player_name", "captains", "player_id")
