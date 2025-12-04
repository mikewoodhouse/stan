from nicegui import ui

from stan.config import config
from stan.pages.sidebar_menu import sidebar
from stan.types import Captain
from stan.utils import add_slot_to_table, page_header, sortable

COLS = [
    sortable("name", align="left"),
    sortable("matches"),
    sortable("won", "W"),
    sortable("lost", "L"),
    sortable("drawn", "D"),
    sortable("nodecision", "N/D"),
    sortable("tied", "T"),
    sortable("won_pct", "Won%"),
    sortable("not_lost_pct", "Not Lost%"),
]


def show_captains():
    page_header(f"Captains ({config.MIN_CAPTAINED} or more games)")

    sidebar()

    rows = Captain.all()

    with ui.column():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "name", "captains", "player_id")
