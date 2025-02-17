from dataclasses import asdict

from nicegui import ui

from app.config import config
from app.pages.sidebar_menu import sidebar
from app.types import AllTimeBowling
from app.utils import add_slot_to_table, balls_to_overs, page_header, sortable

COLS = [
    sortable("name", align="left"),
    sortable("from_yr", "From"),
    sortable("to_yr", "To"),
    sortable("seasons"),
    sortable("overs"),
    sortable("maidens"),
    sortable("wickets"),
    sortable("runs_conceded", "Runs"),
    sortable("bowlave", "Avg", decimals=2),
    sortable("strike_rate", "Strike", decimals=2),
    sortable("econ", decimals=2),
]


def show_bowling():
    page_header(f"Bowling Averages (min: {config.MIN_WICKETS} wickets)")

    sidebar()

    records = AllTimeBowling.all(config.MIN_WICKETS)

    rows = [
        asdict(row)
        | {
            "position": pos + 1,
            "overs": balls_to_overs(row.ballsbowled),
        }
        for pos, row in enumerate(records)
    ]

    with ui.row():
        with ui.table(rows=rows, columns=COLS).props("dense") as table:
            add_slot_to_table(table, "name", "players", ["player_id"])
