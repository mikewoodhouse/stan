from dataclasses import asdict

from nicegui import ui

from app.types import Season
from app.utils import add_slot_to_table, coldef, page_header

from .sidebar_menu import sidebar

SEASON_COLS = [
    coldef("year", align="left"),
    coldef("played", "P"),
    coldef("won", "W"),
    coldef("lost", "L"),
    coldef("drawn", "D"),
    coldef("tied", "T"),
    coldef("noresult", "N/D"),
]


def show_seasons():
    page_header("Seasons")

    sidebar()

    with ui.row():
        seasons = Season.all()

        table = ui.table(
            rows=[asdict(season) for season in seasons],
            columns=SEASON_COLS,
            pagination=30,
        ).props("dense")

        add_slot_to_table(table, "year", "season", "year")
