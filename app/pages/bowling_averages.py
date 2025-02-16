from dataclasses import asdict

from nicegui import ui

from app.config import config
from app.pages.sidebar_menu import sidebar
from app.types import AllTimeBowling
from app.utils import add_slot_to_table, page_header

COLS = []


def show_bowling():
    page_header(f"Bowling Averages (min: {config.MIN_INNINGS} innings)")

    sidebar()

    records = AllTimeBowling.all(config.MIN_INNINGS)
    rows = [asdict(row) | {"position": pos + 1} for pos, row in enumerate(records)]

    with ui.row():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "name", "players", ["player_id"])
