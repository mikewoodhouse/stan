from dataclasses import asdict

from nicegui import ui

from app.config import config
from app.pages.sidebar_menu import sidebar
from app.types import AllTimeBatting
from app.utils import add_slot_to_table, page_header, sortable

COLS = [
    sortable("position"),
    sortable("name", align="left"),
    sortable("from_yr", "From"),
    sortable("to_yr", "To"),
    sortable("seasons"),
    sortable("matches"),
    sortable("innings", "Inns"),
    sortable("notout", "N/O"),
    sortable("high_score", "High"),
    sortable("runsscored", "Runs"),
    sortable("batave", "Avg", decimals=2),
    sortable("fours", "4s"),
    sortable("sixes", "6s"),
    sortable("fifties", "50s"),
    sortable("hundreds", "100s"),
]


def show_batting():
    page_header(f"Batting Averages (min: {config.MIN_INNINGS} innings)")

    sidebar()

    records = AllTimeBatting.all(config.MIN_INNINGS)
    rows = [asdict(row) | {"position": pos + 1} for pos, row in enumerate(records)]

    with ui.row():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "name", "players", ["player_id"])
