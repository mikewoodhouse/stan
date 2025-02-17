from functools import partial

from nicegui import ui

from app.config import config
from app.pages.sidebar_menu import sidebar
from app.types import Captain
from app.utils import add_slot_to_table, coldef, page_header

sortable = partial(coldef, sortable=True)

COLS = [
    sortable("player_name", label="Name", align="left"),
    sortable("matches"),
    sortable("won", label="W"),
    sortable("lost", label="L"),
    sortable("drawn", label="D"),
    sortable("nodecision", label="N/D"),
    sortable("tied", label="T"),
    sortable("won_pct", label="Won%"),
    sortable("not_lost_pct", label="Not Lost%"),
]


def show_captains():
    page_header(f"Captains ({config.MIN_CAPTAINED} or more games)")

    sidebar()

    rows = Captain.all()

    with ui.column():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "player_name", "captains", "player_id")
