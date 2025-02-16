from dataclasses import asdict

from nicegui import ui

from app.config import config
from app.pages.sidebar_menu import sidebar
from app.types import AllTimeFielding
from app.utils import add_slot_to_table, page_header

COLS = []


def show_fielding():
    page_header("Fielding Records")

    sidebar()

    records = AllTimeFielding.all(config.MIN_INNINGS)
    rows = [asdict(row) | {"position": pos + 1} for pos, row in enumerate(records)]

    with ui.row():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "name", "players", ["player_id"])
